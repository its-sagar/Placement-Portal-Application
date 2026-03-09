from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            
            if current_user.role not in roles:
                return abort(403)
                
            if current_user.role == 'company' and not current_user.is_approved:
                # Companies need to be approved before creating drives etc.
                # You may redirect to a "pending approval" page.
                # We'll allow them to see their dashboard but restrict actions.
                # Depends on specific route.
                pass
                
            if not current_user.is_active:
                # Blacklisted
                return abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
