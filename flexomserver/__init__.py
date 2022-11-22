from .config import FlexomServerConfig
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pywebpush import webpush

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = FlexomServerConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{FlexomServerConfig.SQLITE_PATH}"
db.init_app(app)

from .models import *
with app.app_context():
    db.create_all()


vapid_dir = FlexomServerConfig.VAPID_DIR
with open(os.path.join(vapid_dir, "private_key.pem"), "r+") as f:
    vapid_private_key = f.readline().strip("\n")
with open(os.path.join(vapid_dir, "public_key.pem"), "r+") as f:
    vapid_public_key = f.read().strip("\n")
vapid_claims = {
    "sub": FlexomServerConfig.VAPID_CLAIM_EMAIL
}


def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=vapid_private_key,
        vapid_claims=vapid_claims
    )


from .views import *
