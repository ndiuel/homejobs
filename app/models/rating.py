from . import db
from .base import BaseModel



class Rating(db.Model, BaseModel):
    __tablename_ = "ratings"
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id')
    )
    provider_id = db.Column(
        db.Integer(),
        db.ForeignKey('provider.id')
    )
    rating = db.Column(db.Integer)
    provider = db.relationship("Provider", backref='ratings', foreign_keys=[provider_id], remote_side="Provider.id")
    user = db.relationship("User", foreign_keys=[user_id], remote_side="User.id")
    