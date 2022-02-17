from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


from .base import BaseModel
from .user import User
from .role import Role, UserRoles
from .provider import Provider


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
    
    
