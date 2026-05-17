from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user

def role_required(*roles):
    """
    Decorator to restrict access to endpoints based on user roles.
    Takes a list of allowed roles.
    If the current_user's role is not in the list, aborts with 403 Forbidden.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.role not in roles and current_user.role != 'Admin':
                # Admin always has access. Otherwise, check explicit roles.
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
