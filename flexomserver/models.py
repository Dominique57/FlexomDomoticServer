from . import db


class Subscriptions(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
