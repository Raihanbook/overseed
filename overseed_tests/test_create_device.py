from overseed.models import Plant, PlantIcon
from overseed_tests.overseed_test_case import OverseedTestCase

# Create Device test
# ---------------
# This test case covers all the create device tests, for admins and supervisors.
class TestCreateDevice(OverseedTestCase):

    def test_create_device_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        plant = self.add_plant()

        result = self.client.post("create/device", 
                                data=dict(code='900', 
                                        location='Test Location', 
                                        plant=str(plant)), 
                                follow_redirects=True)
        
        self.assert_template_used('devices_list.html')
        self.assert_message_flashed('The device has been created.', 'success')
        self.assertIn(b'Test Location', result.data) 


    def test_create_device_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        plant = self.add_plant()

        result = self.client.post("create/device", 
                                data=dict(code='900', 
                                        location='Test Location', 
                                        plant=str(plant)), 
                                follow_redirects=True)
        
        self.assert_template_used('devices_list.html')
        self.assert_message_flashed('The device has been created.', 'success')
        self.assertIn(b'Test Location', result.data) 


    def test_create_device_admin_invalid_code(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        plant = self.add_plant()

        result = self.client.post("create/device", 
                                data=dict(code='1100', 
                                        location='Test Location', 
                                        plant=str(plant)), 
                                follow_redirects=True)

        self.assert_template_used('create_device.html')
        
        result = self.client.get("/devices")
        self.assertNotIn(b'Test Location', result.data) 

    
    def test_create_device_admin_invalid_plant(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        self.add_plant()

        # Get the first plant that has a device
        plants = Plant.query.all()
        for plant in plants:
            if plant.device != None:
                chosenPlant = plant

        result = self.client.post("create/device", 
                                data=dict(code='900', 
                                        location='Test Location', 
                                        plant=str(chosenPlant)), 
                                follow_redirects=True)

        # Since the plants that are already assigned to devices aren't added to the form, 
        # they will show errors and will be invalid choices.
        self.assert_template_used('create_device.html')
        self.assertIn(b'Not a valid choice', result.data)
        
        result = self.client.get("/devices")
        self.assertNotIn(b'Test Location', result.data) 


    def test_create_device_admin_no_available_plant(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        plant = Plant.query.all()[0]

        result = self.client.post("create/device", 
                                data=dict(code='900', 
                                        location='Test Location', 
                                        plant=str(plant)), 
                                follow_redirects=True)

        self.assert_template_used('devices_list.html')
        self.assert_message_flashed('There are no available plants without devices!', 'danger')
        
        result = self.client.get("/devices")
        self.assertNotIn(b'Test Location', result.data) 


    def test_create_device_user(self):

        self.client.post("/login", 
                        data=dict(email='user@user.com', password='user', remember=False), 
                        follow_redirects=True)

        # This value shouldn't matter, since we should be redirected before it's used.
        plant = "Plant 1"

        result = self.client.post("create/device", 
                                data=dict(code='900', 
                                        location='Test Location', 
                                        plant=str(plant)), 
                                follow_redirects=True)
        
        self.assert403(result)


    def test_create_device_logged_out(self):

        # This value shouldn't matter, since we should be redirected before it's used.
        plant = "Plant 1"

        result = self.client.post("create/device", 
                                data=dict(code='900', 
                                        location='Test Location', 
                                        plant=str(plant)), 
                                follow_redirects=True)
        
        self.assert403(result)


    # -----

    # Helper function to add a plant. Requires the user to first be logged in.
    def add_plant(self):
        result = self.client.post("create/plant", 
                                data=dict(type='Aloe Vera', 
                                        icon='pilea_healthy.png', 
                                        company='Company X'), 
                                follow_redirects=True)

        pileaIcon = PlantIcon.query.filter_by(health_1="pilea_healthy.png").first()

        plant = Plant.query.filter_by(icon_id=pileaIcon.id).first()

        return plant
