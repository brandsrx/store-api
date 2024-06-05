from flask import Blueprint,jsonify,request
from app.models.producto_model import Producto
from app.views.producto_view import render_producto_detail,render_producto_list
from app.utils.decorators import jwt_required, roles_required

producto_bp = Blueprint("producto",__name__)

@producto_bp.route("/products", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_animals():
    productos = Producto.get_all()
    return jsonify(render_producto_list(productos)),200

#Ruta para obtener un animal especifico por su Id
@producto_bp.route("/products/<int:id>",methods=["GET"])
@jwt_required
@roles_required(roles=["admin","user"])
def get_proucto(id):
    producto = Producto.get_by_id(id)
    if producto:
        return jsonify(render_producto_detail(producto))
    return jsonify({"error":"Producto no encontrado"}),404

@producto_bp.route("/products",methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_product():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    print(data)
    if not name or not description or not price or stock is None:
        return jsonify({"error":"Faltan datos requeridos"}),400
    
    producto = Producto(name=name,description=description,price=price,stock=stock)
    producto.save()
    
    return jsonify(render_producto_detail(producto)),201

#Ruta para actualizar un producto existente
@producto_bp.route("/products/<int:id>",methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_product(id):
    producto = Producto.get_by_id(id)
    if not producto:
        return jsonify({"error":"Producto no encontrado"}),404
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    try: 
        producto.update(name=name,description=description,price=price,stock=stock)
        return jsonify(render_producto_detail(producto)),200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    

@producto_bp.route("/products/<int:id>",methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_producto(id):
    producto = Producto.get_by_id(id)
    if not producto:
        return jsonify({"error":"Producto no encontrado"}),404
    
    producto.delete()
    
    return "",204
