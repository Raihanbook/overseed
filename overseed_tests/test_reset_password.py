from overseed_tests.overseed_test_case import OverseedTestCase

# Login test
# ---------------
# This test case covers that the reset password email is sent.
class TestResetPassword(OverseedTestCase):

    def test_reset_password_existing(self):
        result = self.client.post("/reset_password", 
                                data=dict(email='admin@admin.com'), 
                                follow_redirects=True)
        
        self.assertTemplateUsed('login.html')
        self.assertMessageFlashed('An email has been sent (to admin@admin.com) with instructions to reset your password.', 'info')

    def test_reset_password_not_existing(self):
        result = self.client.post("/reset_password", 
                                data=dict(email='fake@test.com'), 
                                follow_redirects=True)
        
        self.assertTemplateUsed('login.html')
        self.assertMessageFlashed('An email has been sent (to fake@test.com) with instructions to reset your password.', 'info')