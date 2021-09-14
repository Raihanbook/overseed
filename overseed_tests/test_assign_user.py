from werkzeug.datastructures import ImmutableMultiDict
from overseed_tests.overseed_test_case import OverseedTestCase

# Assign user test
# ---------------
# This test case covers all the Assign User tests, where admins and supervisors assign 
# users to companies.
class TestAssignUser(OverseedTestCase):

    def test_assign_user_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        data = {
            'companies' : ['<Company 1>', '<Company 2>']
        }

        data = ImmutableMultiDict(data)
                                    
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/3", 
                                data=data, 
                                follow_redirects=True)

        self.assert_template_used('account_list.html')
        self.assert_message_flashed('Successfully assigned user to the selected companies.', 'success')
        self.assertIn(b'company_x.png', result.data)
        self.assertIn(b'company_y.png', result.data)


    def test_assign_user_admin_no_assignments(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        data = {
            'companies' : []
        }

        data = ImmutableMultiDict(data)
                                    
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/3", 
                                data=data, 
                                follow_redirects=True)

        self.assert_template_used('assign_user.html')
        self.assertIn(b'This field is required.', result.data)

    
    def test_assign_admin_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        data = {
            'companies' : ['<Company 1>', '<Company 2>']
        }

        data = ImmutableMultiDict(data)
            
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/1", 
                                data=data, 
                                follow_redirects=True)

        self.assert_message_flashed('You cannot assign companies to this account.', 'danger')


    def test_assign_admin_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        data = {
            'companies' : ['<Company 1>', '<Company 2>']
        }

        data = ImmutableMultiDict(data)
            
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/2", 
                                data=data, 
                                follow_redirects=True)
                                
        self.assert_message_flashed('You cannot assign companies to this account.', 'danger')


    def test_assign_user_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        data = {
            'companies' : ['<Company 1>', '<Company 2>']
        }

        data = ImmutableMultiDict(data)
                                    
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/3", 
                                data=data, 
                                follow_redirects=True)

        self.assert_template_used('account_list.html')
        self.assert_message_flashed('Successfully assigned user to the selected companies.', 'success')
        self.assertIn(b'company_x.png', result.data)
        self.assertIn(b'company_y.png', result.data)


    def test_assign_user_user(self):
        self.client.post("/login", 
                        data=dict(email='user@user.com', password='user', remember=False), 
                        follow_redirects=True)

        data = {
            'companies' : ['<Company 1>', '<Company 2>']
        }

        data = ImmutableMultiDict(data)
                                    
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/3", 
                                data=data, 
                                follow_redirects=True)

        self.assert403(result)


    def test_assign_user_logged_out(self):

        data = {
            'companies' : ['<Company 1>', '<Company 2>']
        }

        data = ImmutableMultiDict(data)
                                    
        # now navigate to the assign user page and assign to valid companies.
        result = self.client.post("/assign_user/3", 
                                data=data, 
                                follow_redirects=True)

        self.assert403(result)