from . import db
from .base import BaseModel

ROLES = [
    'normal', 'admin', 'super_admin'
]

ADMIN_ROLES = [
]


class Role(db.Model, BaseModel):
    __tablename__ = 'roles'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        unique=True
    )

    @classmethod
    def insert_roles(cls):
        for name in ROLES + ADMIN_ROLES:
            role = Role(name=name)
            db.session.add(role)
        db.session.commit()


class UserRoles(db.Model, BaseModel):
    __tablename__ = 'user_roles'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id', ondelete='CASCADE')
    )
    role_id = db.Column(
        db.Integer(),
        db.ForeignKey('roles.id', ondelete='CASCADE')
    )
