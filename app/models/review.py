from . import db
from .base import BaseModel



class Review(db.Model, BaseModel):
    __tablename_ = "reviews"
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
    content = db.Column(db.Text)
    provider = db.relationship("Provider", backref=db.backref(
            'reviews', lazy='dynamic'
        ), foreign_keys=[provider_id], remote_side="Provider.id")
    user = db.relationship("User", backref=db.backref(
            'reviews', lazy='dynamic'
        ), foreign_keys=[user_id], remote_side="User.id")
    