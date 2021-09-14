from flask_mail import Message
from overseed import mail
from flask import url_for, render_template

# This function sends an email to the given user, using the provided input template 
# and subject line. The email will expire after the given expiry seconds.
# ---------------
# Returns nothing.
def send_reset_email(user, template, exp_sec, subject):
    token = user.get_reset_token(exp_sec)
    message = Message(subject, sender='noreply@demo.com', recipients=[user.email])
    message.html = render_template(template, token=token)
    mail.send(message)

# This function checks the given user to see ife they have any of the given privileges.
# ---------------
# Returns True or False.
def check_privilege(user, *privilege_id):
    # Check if the user's privilege ID is in the specified privilege ID
    if user.privilege_id in privilege_id:
        return True
    else:
        return False
