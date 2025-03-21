from flask import Blueprint, request, jsonify
from config import db
from models import Product
from utils import token_required

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.json
    if not all(k in data for k in ['name', 'price', 'quantity']):
        return jsonify({'message': 'Missing required fields'}), 400
    new_product = Product(name=data['name'], description=data.get('description', ''), price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})

@routes_bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    products = Product.query.all()
    output = [{'id': p.id, 'name': p.name, 'description': p.description, 'price': float(p.price), 'quantity': p.quantity} for p in products]
    return jsonify(output)
