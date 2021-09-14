from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from overseed.models import RoleID, User

# This class allows us to build a Create User form using WTForms.
# ---------------
# This is the form used by admins to create new users.
# Custom validation is performed on the email to stop emails from 
# being reused.
class CreateUserForm(FlaskForm):
    email = StringField('EMAIL', validators=[DataRequired(), Email()])
    firstName = StringField("FIRST NAME", validators=[DataRequired(), Length(min=2, max=40)])
    lastName = StringField("LAST NAME", validators=[DataRequired(), Length(min=2, max=40)])
    
    permissions = SelectField("PERMISSIONS:", validators=[DataRequired()], choices=[(RoleID.user.value, 'USER'), (RoleID.supervisor.value, 'SUPERVISOR'), (RoleID.admin.value, 'ADMIN')])

    submit = SubmitField('CREATE USER')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
            