from flask_login import LoginManager
from .. import csrf


login_manager = LoginManager() 
login_manager.session_protection = 'strong' 
login_manager.login_view = 'auth.login'

def init_app(app):
    
    login_manager.init_app(app)
    
    from .auth import auth
    app.register_blueprint(auth)
    
    from .user import user 
    app.register_blueprint(user)
    
    from .admin import admin 
    app.register_blueprint(admin)