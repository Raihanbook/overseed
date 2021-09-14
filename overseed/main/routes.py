from flask import Blueprint, url_for
from flask_login import current_user
from werkzeug.utils import redirect
from overseed.models import RoleID
from overseed.accounts.utils import check_privilege

main = Blueprint('main', __name__)

# Home
# ---------------
# This page is used as a main page for newly logged in users, and as the home link.
# Depending on the type of user, this will redirect to different areas.
# Logged out    -> Login page
# User          -> Plant List
# Supervisor    -> Plant List
# Admin         -> Account List
@main.route("/")
@main.route("/home")
def home():

    if current_user.is_authenticated:
        if check_privilege(current_user, RoleID.admin.value):
            return redirect(url_for("supervisors.account_list"))
        elif check_privilege(current_user, RoleID.supervisor.value):
            return redirect(url_for("supervisors.plants_list"))
        else:
            return redirect(url_for("users.plants_list"))
    else:
        return redirect(url_for("accounts.login"))