import re
from ..views import login_manager
from . import db
from flask import url_for, current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from uuid import uuid4
from .base import BaseModel
from .role import Role
from string import digits, ascii_letters
from random import choice
from json import dumps, loads



class User(UserMixin, db.Model, BaseModel):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(64),
        unique=True,
        index=True
    )
    username = db.Column(
        db.String(64),
        unique=True,
        index=True
    )
    phone_no = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    password_id = db.Column(
        db.String(200)
    )
    is_verified = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        'Role',
        secondary='user_roles',
        backref=db.backref(
            'users', lazy='dynamic'
        )
    )
    
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def remove_role(self, role_name):
        if not self.has_role(role_name):
            return
        role = Role.query.filter_by(name=role_name).first()
        if role:
            role.users.remove(self)
            role.save()

    def add_role(self, role_name):
        if self.has_role(role_name):
            return
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            role = Role(name=role_name)
            role.save()
        role.users.append(self)
        role.save()


    def get_id(self):
        return self.password_id    
        

@login_manager.user_loader
def load_user(password_id):
    return User.query.filter_by(password_id=str(password_id)).first()
