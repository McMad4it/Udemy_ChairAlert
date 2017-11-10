from werkzeug.utils import redirect
from flask import Blueprint, url_for, request, session, render_template
from src.models.users.errors import UserError
from src.models.users.user import User
import src.models.users.decorators as user_decorators

__author__ = 'neil'

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email  # puts email within a session.
                return redirect(url_for(".user_alerts"))  # redirct user to another page (go to function user_alerts. url_for gets url in our service for specific method.

        #  returns an error message for incorrect password or if user does not exist
        except UserError as e:  # return error as object e.
            return e.message

    return render_template("users/login.html")


'''
When user arrives (GET request) then they get the register form returned e.g. the render_template part.
When user submits (POST) then the if statement and logic kicks in.
'''
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email  # puts email within a session.
                return redirect(url_for(".user_alerts"))  # re-direct user to another page (go to function user_alerts).

        #  returns an error if user already exists or if email address is not correct format
        except UserError as e:  # return error as object e.
            return e.message

    return render_template("users/register.html")


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
