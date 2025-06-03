from functools import wraps
from flask import abort, request
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

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

def hash_password(password):
    """Generate a secure hash of the password."""
    return generate_password_hash(password)

def verify_password(stored_password, provided_password):
    """Verify a password against its hash or plain text.
    
    This function handles both hashed passwords and plain text passwords
    for backward compatibility during the transition to secure hashing.
    """
    # If the stored password is already hashed
    if stored_password and stored_password.startswith('pbkdf2:sha256:'):
        return check_password_hash(stored_password, provided_password)
    # For backward compatibility with plain text passwords
    return stored_password == provided_password