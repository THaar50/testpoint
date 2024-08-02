from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, logout_user, login_user
from .loginManager import login_manager
from werkzeug.security import check_password_hash
from testpoint.models import User
from testpoint.storagehandler import get_user, get_user_pw, is_admin
from testpoint.validation import email_is_valid

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id: str):
    """
    Check if user is logged in on every page load.
    :param user_id: User ID given as string.
    :return: User ID or None.
    """
    """"""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """
    Redirect unauthorized users to login page.
    :return: Redirect to login page.
    """
    flash('You must be logged in to view that page.', category='error')
    return redirect(url_for('auth.login'))


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login with the provided username and password if they are correct.
    :return: Redirect to staff page or admin panel.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not email_is_valid(username):
            flash(f'Please provide a valid email address.', category='error')
            return render_template('login.html')

        user = get_user(username=username)
        if not user or not check_password_hash(get_user_pw(username=username), password):
            flash(f'Username or password is incorrect. Please try again.', category='error')
            return render_template('login.html')

        login_user(user)
        session.permanent = True

        if is_admin(username=username):
            return redirect(url_for('routes.admin'))

        return redirect(url_for('routes.staff'))

    return render_template('login.html')


@auth.route("/logout/")
@login_required
def logout():
    """
    Log current user out.
    :return: Redirect to login page.
    """
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('auth.login'))
