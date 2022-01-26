from . import db
from .base import BaseModel

ROLES = [
    'normal', 'admin', 'super_admin'
]

ADMIN_ROLES = [
    'can_reply', 'can_create_package', 'can_edit_settings',
    'can_cancel_investment', 'can_cancel_withdrawal', 'can_confirm_investment',
    'can_confirm_withdrawal', 'can_cancel_merge', 'can_confirm_merge',
    'can_block_user', 'can_verify_user','can_activate_user', 'can_upgrade_user',
    'can_edit_user', 'can_change_password', 'can_change_maturity_date', 'can_change_merge_expiry'
    ,'can_create_withdrawal'
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
