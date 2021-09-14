from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

# This class allows us to build a Login form using WTForms.
# ---------------
# This is the form used to log into the website.
class LoginForm(FlaskForm):
    email = StringField('EMAIL', validators=[DataRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    
    remember = BooleanField('REMEMBER ME')

    submit = SubmitField('LOG IN')

# This class allows us to build a Request Reset Password form using WTForms.
# ---------------
# This is the form logged out users use to request a password reset.
class RequestResetPassForm(FlaskForm):
    email = StringField('EMAIL', validators=[DataRequired(), Email()])

    submit = SubmitField('REQUEST PASSWORD RESET')


# This class allows us to build a Reset Password form using WTForms.
# ---------------
# This is the form users will be directed to in their reset password email, and 
# allows them to change their password.
class ResetPasswordForm(FlaskForm):
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    confirm_password = PasswordField('CONFIRM PASSWORD', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('RESET PASSWORD')
