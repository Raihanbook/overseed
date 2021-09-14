from overseed.admins.forms import CreateUserForm
from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from overseed import bcrypt, db
from overseed.accounts.utils import check_privilege, send_reset_email
from overseed.models import User, RoleID
import uuid

admins = Blueprint('admins', __name__)

# Create User
# ---------------
# This page is where an admin can create new users.
@admins.route("/create/user", methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_authenticated:
        abort(403, description="You do not have permissions to view this page.")

    # Needs a check for admin permissions once Permissions are implemented.
    if current_user.privilege_id != RoleID.admin.value:
        abort(403)

    # Now we create the Create User object.
    form = CreateUserForm()

    # Now we do a check to see if the POST request has just been submitted to this page.
    if form.validate_on_submit():

        # Get the data from the POST request.
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        permissions = request.form.get('permissions')

        # If we get inside this conditional, it means a valid form has been submitted.
        # Now we create the user with a temporary random password, and set the account as inactive.
        hashed_password = bcrypt.generate_password_hash(str(uuid.uuid4().hex)).decode('utf-8')
        user = User(first_name=form.firstName.data, last_name=form.lastName.data, email=form.email.data, password=hashed_password, privilege_id=form.permissions.data, active=0)
        db.session.add(user)
        db.session.commit()
        flash('The new account has been created.', 'success')
        send_reset_email(user, 'registration_email.html', None, 'Password Setup')
        return redirect(url_for("supervisors.account_list"))

    return render_template("create_user.html", title="Create User", form=form)

# Delete User
# ---------------
# This page is where an admin can delete users.
# Note they will not be able to delete themselves.
@admins.route("/users/delete/<string:user_id>", methods=["GET", "POST"])
@login_required
def delete_user(user_id):
    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.admin.value):
        abort(403)

    # If the curent user has the privilege, load the selected user on the page
    selected_user = User.query.filter_by(id=user_id).first_or_404()

    if selected_user.id == current_user.id:
        flash('You are not allowed to delete yourself.', 'danger')
        return redirect(url_for("supervisors.account_list"))

    # Clear all of the assignments in the selected user's field
    selected_user.user_assignments.clear()
    selected_user.taken_plants.clear()

    db.session.delete(selected_user)
    db.session.commit()

    flash('User has been successfully deleted.', 'success')
    return redirect(url_for("supervisors.account_list"))
