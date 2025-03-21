from config import app
from auth import auth_bp
from routes import routes_bp
from flask import jsonify

# تسجيل الـ Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

# إضافة مسار رئيسي لتجنب خطأ 404 عند زيارة /
@app.route('/')
def home():
    return jsonify({'message': 'API is running successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
