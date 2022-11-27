from __future__ import annotations
from typing import Optional
from . import db


class Subscriptions(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String, nullable=False)
    expiration_time = db.Column(db.String, nullable=True)
    keys_auth = db.Column(db.String, nullable=False)
    keys_p256dh = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Subscriptions(id={self.id}, endpoint={self.endpoint}, expiration_time=" \
               f"{self.expiration_time}, keys_auth={self.keys_auth}, keys_p256dh=" \
               f"{self.keys_p256dh})"

    @staticmethod
    def from_token(token: dict) -> Optional[Subscriptions]:
        endpoint = token.get('endpoint')
        expiration_time = token.get('expirationTime')
        keys_auth = token.get('keys', {}).get('auth')
        keys_p256dh = token.get('keys', {}).get('p256dh')
        if endpoint is None or keys_auth is None or keys_p256dh is None:
            return None
        return Subscriptions(
            endpoint=endpoint,
            expiration_time=expiration_time,
            keys_auth=keys_auth,
            keys_p256dh=keys_p256dh,
        )

    def to_token(self) -> dict:
        return {
            'endpoint': self.endpoint,
            'expirationTime': self.expiration_time,
            'keys': {
                'auth': self.keys_auth,
                'p256dh': self.keys_p256dh,
            },
        }

    def is_same_token(self, other: Subscriptions) -> bool:
        if other is None:
            return False
        return (self.endpoint == other.endpoint
                and self.keys_auth == other.keys_auth
                and self.keys_p256dh == other.keys_p256dh)
