from overseed.models import User
from overseed_tests.overseed_test_case import OverseedTestCase

# Account List test
# ---------------
# This test case covers all the account list pages (both Admin and Supervisor)
class TestAccountList(OverseedTestCase):

    def test_account_list_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the users page
        result = self.client.get("/users")

        # Assert the account_list template has been used.
        self.assert_template_used('account_list.html')
        
        # check that all users in the database are here.
        for user in User.query.all():
            self.assertIn(str.encode(user.first_name), result.data)
            self.assertIn(str.encode(user.last_name), result.data)

    def test_account_list_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the users page
        result = self.client.get("/users")

        # Assert the account_list template has been used.
        self.assert_template_used('account_list.html')
        
        # check that all users in the database are here.
        for user in User.query.all():
            self.assertIn(str.encode(user.first_name), result.data)
            self.assertIn(str.encode(user.last_name), result.data)

    def test_account_list_user(self):
        self.client.post("/login", 
                        data=dict(email='user@user.com', password='user', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the users page
        result = self.client.get("/users")

        # Assert that the user wasn't allowed.
        self.assert403(result)        

    def test_account_list_logged_out(self):
                                    
        # Go to the users page
        result = self.client.get("/users")

        # Assert that a 403 occured, as there is no logged in user.
        self.assert403(result)