from overseed.models import Plant
from flask_login import current_user
from overseed_tests.overseed_test_case import OverseedTestCase

# Account List test
# ---------------
# This test case covers all the plant list pages (Admin, Supervisor, and User)
class TestPlantsList(OverseedTestCase):

    def test_all_plants_list_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the plants page
        result = self.client.get("/plants")

        # Assert the plants_list template has been used.
        self.assert_template_used('plants_list.html')
        
        # check that all plants in the database are here.
        for plant in Plant.query.all():
            self.assertIn(str.encode(plant.plant_type.name), result.data)
            self.assertIn(str.encode(plant.device.description), result.data)


    def test_all_plants_list_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)
                                    
        # Go to the plants page
        result = self.client.get("/plants")

        # Assert the plants_list template has been used.
        self.assert_template_used('plants_list.html')
        
        # check that all plants in the database are here.
        for plant in Plant.query.all():
            self.assertIn(str.encode(plant.plant_type.name), result.data)
            self.assertIn(str.encode(plant.device.description), result.data)


    def test_all_plants_list_user(self):
        self.client.post("/login", 
                            data=dict(email='user@user.com', password='user', remember=False), 
                            follow_redirects=True)

        # Go to the plants page
        result = self.client.get("/plants")

        # Assert that users are unable to access the /plants route (that's for admins & supervisors only)
        self.assert403(result)


    def test_all_plants_list_logged_out(self):
                                    
        # Go to the plants page
        result = self.client.get("/plants")

        # Assert the plants_list template has been used.
        self.assert403(result)


    def test_plants_list_user(self):
        # Use with self.client to be able to access the current_user
        with self.client:
            self.client.post("/login", 
                            data=dict(email='user@user.com', password='user', remember=False), 
                            follow_redirects=True)
                                        
            # Go to the plants page
            result = self.client.get("/user/plants")

            # Assert the plants_list template has been used.
            self.assert_template_used('plants_list.html')
            
            # for each plant assigned to that user, make sure it is there.
            for company in current_user.user_assignments:
                for plant in Plant.query.filter_by(company_id = company.id):
                    # we check both the type and the location, which together should make sure they're all there.
                    #
                    # There are edge cases that aren't caught. for example, for plants A, B, & C, where A & B share 
                    # a location, and B & C share a type. In this case, B, could be missing but wouldn't be detected.
                    self.assertIn(str.encode(plant.plant_type.name), result.data)
                    self.assertIn(str.encode(plant.device.description), result.data)


    def test_plants_list_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        # Go to the user plants page
        result = self.client.get("/user/plants")

        # Assert that supervisors are unable to access the /user/plants route (that's for users only)
        self.assert403(result)


    def test_plants_list_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # Go to the plants page
        result = self.client.get("/user/plants")

        # Assert that admins are unable to access the /user/plants route (that's for users only)
        self.assert403(result)


    def test_plants_list_logged_out(self):
                                    
        # Go to the user plants page
        result = self.client.get("/user/plants")

        # Assert the plants_list template has been used.
        self.assert403(result)