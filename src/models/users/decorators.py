from functools import wraps
from flask import session, url_for, redirect, request
from src.app import app

__author__ = 'neil'


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)  # args func(5,6) kwargs: func(x=5,y=6)
    return decorated_function


def requires_admin_permission(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user', message="You need to be an admin to access that"))
        return func(*args, **kwargs)  # args func(5,6) kwargs: func(x=5,y=6)
    return decorated_function


