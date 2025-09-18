
# Utils Files

## utils/security.py

```python
import bcrypt
import re
from flask import request
from functools import wraps
from flask_login import current_user

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, user_password):
    """Check if the provided password matches the hashed password"""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate South African phone number format"""
    pattern = r'^(\+27|0)[6-8][0-9]{8}$'
    return re.match(pattern, phone) is not None

def requires_roles(*roles):
    """Decorator to require specific user roles"""
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                return "Unauthorized", 403
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def sanitize_input(input_str):
    """Basic input sanitization to prevent XSS"""
    if not input_str:
        return input_str
    return input_str.replace('<', '&lt;').replace('>', '&gt;')
