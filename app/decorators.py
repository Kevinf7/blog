from functools import wraps
from flask import abort
from flask_login import current_user

#this code is taken from Flask Web Development book by O'Reilly
#it allows you to add decorator to any route, and will return 403 error if user is not that role
def permission_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_role(role):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required('admin')(f)
