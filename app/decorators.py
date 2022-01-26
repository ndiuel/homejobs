from flask import abort
from flask_login import login_required, current_user
from functools import wraps

def roles_required(*roles, require_all=True):
    def decorated(func):
        @login_required
        @wraps(func) 
        def inner(*args, **kwargs):
            if require_all:
                current_user_has_role = all(
                    current_user.has_role(role) for role in roles
                )
            else:
                current_user_has_role = any(
                    current_user.has_role(role) for role in roles
                )
            if current_user_has_role:
                return func(*args, **kwargs)
            abort(403)
        return inner
    return decorated

            
