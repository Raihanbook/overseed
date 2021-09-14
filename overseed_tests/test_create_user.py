from overseed.models import RoleID
from overseed_tests.overseed_test_case import OverseedTestCase

# Create User test
# ---------------
# This test case covers the Create User, which only Admins are able to do.
class TestCreateUser(OverseedTestCase):

    def test_create_user_user(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create user page and create a new user (with new valid data)
        result = self.client.post("create/user", 
                                data=dict(firstName='User', 
                                        lastName='Guy', 
                                        email='user2@user.com', 
                                        permissions=RoleID.user.value), 
                                follow_redirects=True)
        
        self.assert_template_used('account_list.html')
        self.assert_message_flashed('The new account has been created.', 'success')
        self.assertIn(b'User Guy', result.data) 

    def test_create_supervisor_user(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # now navigate to the create user page and create a new supervisor (with new valid data)
        result = self.client.post("create/user", 
                                data=dict(firstName='Supervisor', 
                                        lastName='Guy', 
                                        email='supervisor2@supervisor.com', 
                                        permissions=RoleID.supervisor.value), 
                                follow_redirects=True)
        
        self.assert_template_used('account_list.html')
        self.assert_message_flashed('The new account has been created.', 'success')
        self.assertIn(b'Supervisor Guy', result.data) 


    def test_create_admin_user(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create user page and create a new admin (with new valid data)
        result = self.client.post("create/user", 
                                data=dict(firstName='Admin', 
                                        lastName='Guy', 
                                        email='adminster@admin.com', 
                                        permissions=RoleID.admin.value), 
                                follow_redirects=True)
        
        self.assert_template_used('account_list.html')
        self.assert_message_flashed('The new account has been created.', 'success')
        self.assertIn(b'Admin Guy', result.data) 

    def test_create_existing_user_user(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # try to create a user with the user@user.com email (which already exists)
        self.client.post("create/user", 
                                data=dict(firstName='User', 
                                        lastName='User2', 
                                        email='user@user.com', 
                                        permissions=RoleID.user.value), 
                                follow_redirects=True)
        self.assert_template_used('create_user.html')

        result = self.client.get("/users")
        self.assertNotIn(b'User User2', result.data) 


    def test_create_user_as_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        # now navigate to the create user page and create a new user (with valid data, but we're logged out)
        result = self.client.post("create/user", 
                                data=dict(firstName='User', 
                                        lastName='Guy', 
                                        email='user5@user.com', 
                                        permissions=RoleID.user.value), 
                                follow_redirects=True)
        
        self.assert403(result)


    def test_create_user_as_user(self):
        self.client.post("/login", 
                        data=dict(email='user@user.com', password='user', remember=False), 
                        follow_redirects=True)

        # now navigate to the create user page and create a new user (with valid data, but we're logged out)
        result = self.client.post("create/user", 
                                data=dict(firstName='User', 
                                        lastName='Guy', 
                                        email='user5@user.com', 
                                        permissions=RoleID.user.value), 
                                follow_redirects=True)
        
        self.assert403(result)

    def test_create_logged_out(self):
        # DON'T log in here.

        # now navigate to the create user page and create a new user (with valid data, but we're logged out)
        result = self.client.post("create/user", 
                                data=dict(firstName='User', 
                                        lastName='Guy', 
                                        email='user5@user.com', 
                                        permissions=RoleID.user.value), 
                                follow_redirects=True)
        
        self.assert403(result)
        