from overseed import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from enum import Enum

# This function is the user loader function. It takes in a user id.
# ---------------
# This function returns the user with the given user id. It is used by flask_login
# to load in the current user.
@login_manager.user_loader
def load_user (user_id):
    return User.query.get(int(user_id))

# Assignments
# ---------------
# This class is an SQLAlchemy table that allows us to have a many-to-many relationship 
# between users and the companies they are assigned to.
assignments = db.Table('assignment',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'))
)

# User Table
# ---------------
# This class is an SQLAlchemy table that allows us to store User information.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    privilege_id = db.Column(db.Integer, db.ForeignKey('privilege.id'))
    active = db.Column(db.Integer, nullable=False)
    user_assignments = db.relationship('Company', secondary=assignments, backref='assigned_to')

    taken_plants = db.relationship('Plant', backref='user')
    
    def get_reset_token(self, expires_sec):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

# Privilege Table
# ---------------
# This class is an SQLAlchemy table that allows us to store Privilege information.
class Privilege(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    notes = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', backref='privilege')

# Device Table
# ---------------
# This class is an SQLAlchemy table that allows us to store Device information.
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(), nullable=False)
    hardware_id = db.Column(db.String(), unique=True)
    plant = db.relationship("Plant", uselist=False, back_populates="device")

# Company Table
# ---------------
# This class is an SQLAlchemy table that allows us to store Company information.
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(), unique=True, nullable=False)
    phone_number = db.Column(db.String())
    contact_email = db.Column(db.String())
    contact_name = db.Column(db.String())
    address = db.Column(db.String(), nullable=False)
    icon = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String())
    active = db.Column(db.Integer, nullable=False)

    plants = db.relationship('Plant', backref='company')

# Plant Icon Table
# ---------------
# This class is an SQLAlchemy table that allows us to store Plant Icon information.
class PlantIcon(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Name of file (do not include path in this field)
    health_1 = db.Column(db.String(), nullable=False)
    health_2 = db.Column(db.String(), nullable=False)
    health_3 = db.Column(db.String(), nullable=False)

    plants = db.relationship('Plant', backref='icon')

# Plant Table
# ---------------
# This class is an SQLAlchemy table that allows us to store Plant information.
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.relationship("Device", back_populates="plant")

    # I'm not sure if these are actually necessary, the backrefs should be enough.
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), index=True)
    icon_id = db.Column(db.Integer, db.ForeignKey('plant_icon.id'), index=True)
    plant_type_id = db.Column(db.Integer, db.ForeignKey('plant_type.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

# PlantType Table
# ---------------
# This class is an SQLAlchemy table that allows us to store Plant Type information.
class PlantType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    care_instructions = db.Column(db.String(), nullable=False)

    humidity_high = db.Column(db.Float(), nullable=False)
    humidity_low = db.Column(db.Float(), nullable=False)
    temperature_high = db.Column(db.Float(), nullable=False)
    temperature_low = db.Column(db.Float(), nullable=False)
    moisture_high = db.Column(db.Float(), nullable=False)
    moisture_low = db.Column(db.Float(), nullable=False)
    minimum_light = db.Column(db.Float(), nullable=False)

    plants = db.relationship('Plant', backref='plant_type')

# RoleID Enum
# ---------------
# This Enum provides us with a way to quickly compare user privileges.
class RoleID(Enum):
    admin = 1
    supervisor = 2
    user = 3
