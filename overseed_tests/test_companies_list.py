from overseed.models import Company
from overseed_tests.overseed_test_case import OverseedTestCase

# Account List test
# ---------------
# This test case covers all the create company pages (both Admin and Supervisor)
class TestCompaniesList(OverseedTestCase):

    def test_companies_list_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the users page
        result = self.client.get("/companies")

        # Assert the companies_list template has been used.
        self.assert_template_used('companies_list.html')
        
        # check that all users in the database are here.
        for company in Company.query.all():
            self.assertIn(str.encode(company.name), result.data)
            self.assertIn(str.encode(company.icon), result.data)


    def test_companies_list_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the users page
        result = self.client.get("/companies")

        # Assert the companies_list template has been used.
        self.assert_template_used('companies_list.html')
        
        # check that all users in the database are here.
        for company in Company.query.all():
            self.assertIn(str.encode(company.name), result.data)
            self.assertIn(str.encode(company.icon), result.data)


    def test_companies_list_user(self):
        self.client.post("/login", 
                        data=dict(email='user@user.com', password='user', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the companies page
        result = self.client.get("/companies")

        # Assert that the user wasn't allowed.
        self.assert403(result)        


    def test_companies_list_logged_out(self):
                                    
        # Go to the companies page
        result = self.client.get("/companies")

        # Assert that a 403 occured, as there is no logged in user.
        self.assert403(result)