from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # السماح بالطلبات عبر المتصفح

# إعداد قاعدة البيانات بدون كلمة مرور
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/security_db'
app.config['SECRET_KEY'] = '6aca54eca039e46261b03d97a2058021696d65261cad3a95eb266c12528a2954'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)