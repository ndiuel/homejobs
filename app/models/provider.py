from email.policy import default
from lib2to3.pytree import Base
from . import db
from .base import BaseModel


class Provider(db.Model, BaseModel):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", uselist=False)
    about = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=False)
    identification_doc_url = db.Column(db.Text)
    state = db.Column(db.String(200))
    lga = db.Column(db.String(200))
    address = db.Column(db.String(300))
    