from flask import abort
from flask_login import current_user
from app.models import Staff
from werkzeug.security import generate_password_hash, check_password_hash

def is_admin_user():
    return getattr(current_user, 'is_admin', False)

def current_user_id():
    return getattr(current_user, 'id', None)

def format_date(date_obj):
    return date_obj.strftime("%d-%m-%Y") if date_obj else ""


def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def require_role(role):
    """
    Ensure the current user has the specified role.
    :param role: The required role (e.g., 'Admin', 'Faculty', 'Student').
    """
    if not hasattr(current_user, 'role') or current_user.role != role:
        abort(403)  # Forbidden
