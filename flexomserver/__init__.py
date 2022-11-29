from .config import FlexomServerConfig
import os
import requests
from pywebpush import webpush
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler


class Config:
    SECRET_KEY = FlexomServerConfig.SECRET_KEY

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{FlexomServerConfig.SQLITE_PATH}"

    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 1}}
    SCHEDULER_JOB_DEFAULTS = {"coalesce": False, "max_instances": 1}
    SCHEDULER_API_ENABLED = True


db = SQLAlchemy()
scheduler = APScheduler()

app = Flask(__name__)
app.config.from_object(Config())

db.init_app(app)
scheduler.init_app(app)
scheduler.start()

from .models import *
with app.app_context():
    db.create_all()


vapid_dir = FlexomServerConfig.VAPID_DIR
with open(os.path.join(vapid_dir, "private_key.pem"), "r+") as f:
    vapid_private_key = f.readline().strip("\n")
with open(os.path.join(vapid_dir, "public_key.pem"), "r+") as f:
    vapid_public_key = f.read().strip("\n")
vapid_claims = {
    "sub": f"mailto:{FlexomServerConfig.VAPID_CLAIM_EMAIL}",
}


def send_web_push(subscription_information, message_body) -> requests.Response:
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=vapid_private_key,
        vapid_claims=vapid_claims
    )


from .views import *
