from overseed_tests.overseed_test_case import OverseedTestCase

# Login test
# ---------------
# This test case covers all login functionality, as well as logout functionality.
class TestLogin(OverseedTestCase):

    def test_login_admin(self):

        response = self.client.post("/login", 
                                    data=dict(email='admin@admin.com', password='admin', remember=False), 
                                    follow_redirects=True)
        self.assert_template_used('account_list.html')

        self.client.post("/logout")

    def test_login_supervisor(self):
        response = self.client.post("/login", 
                                    data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                                    follow_redirects=True)
        self.assert_template_used('plants_list.html')

        self.client.post("/logout")
    
    def test_login_user(self):
        response = self.client.post("/login", 
                                    data=dict(email='user@user.com', password='user', remember=False), 
                                    follow_redirects=True)
        self.assert_template_used('plants_list.html')

        self.client.post("/logout")
    
    def test_login_incorrect_password(self):
        response = self.client.post("/login", 
                                    data=dict(email='admin@admin.com', password='wrong', remember=False), 
                                    follow_redirects=True)
        self.assert_template_used('login.html')

        self.client.post("/logout")

    def test_login_incorrect_email(self):
        response = self.client.post("/login", 
                                    data=dict(email='wrong@admin.com', password='admin', remember=False), 
                                    follow_redirects=True)
        self.assert_template_used('login.html')

        self.client.post("/logout")

    def test_login_incorrect_credentials(self):
        response = self.client.post("/login", 
                                    data=dict(email='wrong@wrong.com', password='wrong', remember=False), 
                                    follow_redirects=True)
        self.assert_template_used('login.html')

        self.client.post("/logout")

    def test_logout(self):
        with self.client:
            response = self.client.post("/login", 
                                        data=dict(email='user@user.com', password='user', remember=False), 
                                        follow_redirects=True)

            self.assert_template_used('plants_list.html')

            #logged in, now to log back out.
            logout = self.client.get("/logout", follow_redirects=True)
            self.assert_template_used("login.html")
        