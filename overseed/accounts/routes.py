from flask import Blueprint, render_template, redirect, url_for, flash
from flask.globals import request
from overseed.accounts.forms import LoginForm, RequestResetPassForm, ResetPasswordForm
from overseed.models import User
from overseed import db, bcrypt
from flask_login import current_user, logout_user, login_user
from overseed.accounts.utils import send_reset_email

accounts = Blueprint('accounts', __name__)

# Login
# ---------------
# This page is where the user logs in.
@accounts.route("/login", methods=['GET', 'POST'])
def login():
    # First, check if the user is already logged in. If so, redirect them to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Now we create the LoginForm object.
    form = LoginForm()

    # Now we do a check to see if the Form has just been submitted to this page.
    if form.validate_on_submit():

        # Get the data from the POST request.
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # If we get inside this conditional, it means a valid form has been submitted.
        # This will get the first User with the given email. If none exists, user = None.
        # Then we will run a conditional that checks if the user exists and if the passwords match
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # The password and user matches.
            # Now we log in the user, using the 'remember' field from the form.
            login_user(user, remember=remember)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid Username/Password!', 'danger')
    
    return render_template('login.html', title='LOG IN', form=form)

# Logout
# ---------------
# This link logs the user out and redirects them to the home page.
@accounts.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home')) 

# Reset Password Request
# ---------------
# This page is where a logged out user can request a password reset.
@accounts.route("/reset_password", methods=['GET', 'POST'])
def reset_pass_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetPassForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('An email has been sent (to ' + form.email.data + ') with instructions to reset your password.', 'info')
            return redirect(url_for('accounts.login'))
        else:
            send_reset_email(user, 'reset_pass_email.html', 1800, 'Password Reset')
            flash('An email has been sent (to ' + form.email.data + ') with instructions to reset your password.', 'info')
            return redirect(url_for('accounts.login'))
    return render_template('reset_pass_request.html', title='Reset Password', form=form)

# Reset Password
# ---------------
# This page is where the reset password email redirects to, with a token.
# If the token is valid, the user can reset their password.
@accounts.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('accounts.reset_pass_request'))
        
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        if user.active == 0:
            user.active = 1
            db.session.commit()
            flash('Your password has been set up! You are now able to log in', 'success')
            return redirect(url_for('accounts.login'))

        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('accounts.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
