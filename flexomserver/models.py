from . import db


class Subscriptions(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String, nullable=False)
    expiration_time = db.Column(db.String, nullable=True)
    keys_auth = db.Column(db.String, nullable=False)
    keys_p256dh = db.Column(db.String, nullable=False)
