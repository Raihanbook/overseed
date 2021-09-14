from overseed_tests.overseed_test_case import OverseedTestCase

# Create Plant test
# ---------------
# This test case covers all the Create Plant pages (both Admin and Supervisor)
class TestCreatePlant(OverseedTestCase):

    def test_create_plant_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create plant page and create a new plant (with new valid data)
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='bush_healthy.png', 
                                        company='Company X'), 
                                follow_redirects=True)
        
        self.assert_template_used('plants_list.html')
        self.assert_message_flashed('The new plant has been created.', 'success')
        self.assertIn(b'bush_healthy.png', result.data) 


    def test_create_plant_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create plant page and create a new plant (with new valid data)
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='bush_healthy.png', 
                                        company='Company X'), 
                                follow_redirects=True)
        
        self.assert_template_used('plants_list.html')
        self.assert_message_flashed('The new plant has been created.', 'success')
        self.assertIn(b'bush_healthy.png', result.data) 


    def test_create_plant_admin_invalid_type(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create plant page and create a new plant (with invalid type data)
        result = self.client.post("create/plant", 
                                data=dict(type='Fictional Plant', 
                                        icon='pilea_healthy.png', 
                                        company='Company X'), 
                                follow_redirects=True)
        
        self.assert_template_used('create_plant.html')

        result = self.client.get("/plants")
        self.assertNotIn(b'Fictional Plant', result.data) 


    def test_create_plant_admin_invalid_icon(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create plant page and create a new plant (with invalid icon data)
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='fictional.png', 
                                        company='Company X'), 
                                follow_redirects=True)
        
        self.assert_template_used('create_plant.html')

        result = self.client.get("/plants")
        self.assertNotIn(b'fictional.png', result.data) 


    def test_create_plant_admin_invalid_company(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create plant page and create a new plant (with invalid company data)
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='tree_healthy.png', 
                                        company='Fictional Company'), 
                                follow_redirects=True)
        
        self.assert_template_used('create_plant.html')

        result = self.client.get("/plants")
        self.assertNotIn(b'Fictional Company', result.data) 


    def test_create_plant_user(self):
        self.client.post("/login", 
                        data=dict(email='user@user.com', password='user', remember=False), 
                        follow_redirects=True)
                                    
        # now navigate to the create plant page and create a new plant (with new valid data)
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='bush_healthy.png', 
                                        company='Company X'), 
                                follow_redirects=True)
        
        self.assert403(result)


    def test_create_plant_logged_out(self):
        # DON'T log in.
                                    
        # now navigate to the create plant page and create a new plant (with new valid data)
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='bush_healthy.png', 
                                        company='Company X'), 
                                follow_redirects=True)
        
        self.assert403(result)
