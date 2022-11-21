from .config import FlexomServerConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = FlexomServerConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{FlexomServerConfig.SQLITE_PATH}"
db.init_app(app)


from .models import *


with app.app_context():
    db.create_all()


from .views import *
