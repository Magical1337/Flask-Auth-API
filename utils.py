import jwt
import datetime
import qrcode
import pyotp
from functools import wraps
from flask import request, jsonify
from io import BytesIO
import base64
from config import app
from models import User

def generate_qr(username, secret):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name="SecureApp")
    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def generate_token(username):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    return jwt.encode({'username': username, 'exp': exp_time}, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(username=data['username']).first()
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
