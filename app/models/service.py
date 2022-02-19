from . import db
from .base import BaseModel


class Service(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    

class ProviderService(db.Model, BaseModel):
    __tablename__ = "provider_services"
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('provider.id', ondelete='CASCADE')
    )
    service_id = db.Column(
        db.Integer(),
        db.ForeignKey('service.id', ondelete='CASCADE')
    )