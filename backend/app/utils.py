from functools import wraps
from flask import abort, request
from flask_login import current_user

def require_role(role):
    """Decorator to require a specific role for a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator