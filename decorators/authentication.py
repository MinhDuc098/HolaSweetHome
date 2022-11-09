from functools import wraps
from flask import request, jsonify, session, render_template
from models.user import UserRole

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session:
            if session.get('banned') == False:
                return f(*args, **kwargs)
            else:
                return render_template("exceptions/exception.html", error=403, message="You have been banned"), 403
        else:
            return render_template('exceptions/exception.html', error=401, message="Unauthorized"), 401
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_required(f)
        if session.get("role") != UserRole.ADMIN:
            return render_template("exceptions/exception.html", error=403, message="Admin role required"), 403
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_required(f)
        if session.get("role") != UserRole.SELLER:
            return render_template("exceptions/exception.html", error=403, message="Seller role required"), 403
        return f(*args, **kwargs)
    return decorated_function


