from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
from config import db
from models import User
from utils import generate_qr, generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    hashed_password = generate_password_hash(password, method='sha256')
    twofa_secret = pyotp.random_base32()

    new_user = User(username=username, password=hashed_password, twofa_secret=twofa_secret)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@auth_bp.route('/generate_qr/<username>', methods=['GET'])
def generate_qr_code(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    qr_code = generate_qr(username, user.twofa_secret)
    return jsonify({'qr_code': qr_code})

@auth_bp.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    data = request.json
    username = data.get('username')
    token = data.get('token')
    user = User.query.filter_by(username=username).first()
    if not user or not pyotp.TOTP(user.twofa_secret).verify(token):
        return jsonify({'message': 'Invalid 2FA token'}), 401
    return jsonify({'message': '2FA verification successful'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    token = data.get('token')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    if not pyotp.TOTP(user.twofa_secret).verify(token):
        return jsonify({'message': 'Invalid 2FA token'}), 401
    jwt_token = generate_token(username)
    return jsonify({'token': jwt_token})
