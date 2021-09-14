from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from overseed.models import Company, Device

# This class allows us to build a Create Plant form using WTForms.
# ---------------
# This is the form used by admins and supervisors to add new Plants.
# The available icons are hard coded on the 8 art assets available.
# The company field values are set up dynamically in the routes.py file.
class CreatePlantForm(FlaskForm):

    type = SelectField("TYPE:", validators=[DataRequired()])
    icon = RadioField("ICON:", validators=[DataRequired()], choices=[
        ('cactus_healthy.png'), 
        ('pilea_healthy.png'), 
        ('bush_healthy.png'),
        ('tree_healthy.png'),
        ('prickly_pear_healthy.png'), 
        ('aloe_healthy.png'), 
        ('bonsai_healthy.png'),
        ('leaves_healthy.png')])
    company = SelectField("COMPANY:", validators=[DataRequired()])

    submit = SubmitField('CREATE PLANT')

# This class allows us to build a Create Device form using WTForms.
# ---------------
# This is the form used by admins and supervisors to create new devices.
# Custom validation is performed on the device code to ensure it doesn't
# already exist.
# The plant field values are set up dynamically in the routes.py file.
class CreateDeviceForm(FlaskForm):

    code = StringField("DEVICE CODE:", validators=[DataRequired()])
    location = StringField("LOCATION:", validators=[DataRequired(), Length(min=2)])
    plant = SelectField("PLANT:", validators=[DataRequired()])

    submit = SubmitField('CREATE DEVICE')

    def validate_code(self, code):
        device = Device.query.filter_by(hardware_id=code.data).first()
        if device:
            raise ValidationError('That device is already in the database (#' + device.hardware_id + '). Please choose a different one.')

# This class allows us to build an Assign User form using WTForms.
# ---------------
# This is the form used by admins and supervisors to assign users.
# The companies field values are set up dynamically in the routes.py file.
class AssignUserForm(FlaskForm):

    companies = SelectField("COMPANIES:", validators=[DataRequired()])

    submit = SubmitField('ASSIGN USER')

# This class allows us to build a Create Company form using WTForms.
# ---------------
# This is the form used by admins and supervisors to create new companies.
# Custom validation is performed on the name to stop names from being reused.
class CreateCompanyForm(FlaskForm):

    name = StringField("COMPANY NAME: *", validators=[DataRequired()])
    icon = FileField('ICON: *', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'JPG or PNG files only!')])
    address = StringField("COMPANY ADDRESS: *", validators=[DataRequired()])
    contact_email = StringField("CONTACT EMAIL: *", validators=[DataRequired(), Email()])

    phone_number = StringField("PHONE NUMBER:")
    contact_name = StringField("CONTACT NAME:")
    notes = StringField("NOTES:")

    submit = SubmitField('CREATE COMPANY')
    
    def validate_name(self, name):
        company = Company.query.filter_by(name=name.data).first()
        if company:
            raise ValidationError('That company is already in the database (' + company.name + '). Please enter a different name.')
