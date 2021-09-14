from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flask_talisman import Talisman
import mimetypes

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'accounts.login'
login_manager.login_message_category = 'danger'
mail = Mail()
# We need to tell the application what are valid mimetypes
mimetypes.add_type("application/x-javascript", ".js", True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6aa9563e3457a413b381a18cc6848a72'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from overseed.main.routes import main
    from overseed.accounts.routes import accounts
    from overseed.users.routes import users
    from overseed.supervisors.routes import supervisors
    from overseed.admins.routes import admins
    from overseed.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(accounts)
    app.register_blueprint(users)
    app.register_blueprint(supervisors)
    app.register_blueprint(admins)
    app.register_blueprint(errors)

    # The Content Security Policy must be configured to avoid CSS attacks but
    # allow valid sources of scripts from CDN's
    csp = {
        'default-src': [
            "'self'",
            "'unsafe-inline'",
            'stackpath.bootstrapcdn.com',
            'code.jquery.com',
            'cdn.jsdelivr.net',
            'fonts.googleapis.com',
            'cdn.jsdelivr.net/npm/chart.js',
            'fonts.gstatic.com',
            'cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js'
        ]
    }

    Talisman(app, content_security_policy=csp)

    return app
