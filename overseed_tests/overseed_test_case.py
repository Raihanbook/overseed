from flask_testing import TestCase
from overseed import create_app
from overseed.utils import delete_and_create_db


# Overseed Test Case
# ---------------
# This class is the parent test case that all our tests inherit from.
# This provides us with the ability to do some things before each test 
# (for example, reset the test database). It also lets us set up app config 
# variables.
class OverseedTestCase(TestCase):

    def setUp(self):
        delete_and_create_db()

    def create_app(self):
        app = create_app()
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['LOGIN_DISABLED'] = True
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app