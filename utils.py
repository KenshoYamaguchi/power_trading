from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required_with_message(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('この機能を使用するにはログインが必要です')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function