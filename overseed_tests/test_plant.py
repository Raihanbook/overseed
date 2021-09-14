from overseed.models import Plant
from overseed_tests.overseed_test_case import OverseedTestCase
from flask_login import current_user

# Plant Page test
# ---------------
# This test case covers testing the plant page, as well as the job system of the plant page.
class TestPlant(OverseedTestCase):

    def test_plant_admin(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # Check all the plants are there.
        for plant in Plant.query.all():
            # Go to the plant page
            result = self.client.get("/plant/" + str(plant.id))

            # Assert the plant template has been used.
            self.assert_template_used('plant.html')

            # Assert the correct plant is shown
            self.assertIn(str.encode(plant.plant_type.name), result.data)

    def test_plant_supervisor(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        # Check all the plants are there.
        for plant in Plant.query.all():
            # Go to the plant page
            result = self.client.get("/plant/" + str(plant.id))

            # Assert the plant template has been used.
            self.assert_template_used('plant.html')

            # Assert the correct plant is shown
            self.assertIn(str.encode(plant.plant_type.name), result.data)


    def test_plant_user(self):
        with self.client:
            self.client.post("/login", 
                            data=dict(email='user@user.com', password='user', remember=False), 
                            follow_redirects=True)

            # Check all the plants are there.
            for plant in Plant.query.all():
                # Go to the plant page
                result = self.client.get("/plant/" + str(plant.id))

                if plant.company in current_user.user_assignments:
                    # Assert the plant template has been used.
                    self.assert_template_used('plant.html')

                    # Assert the correct plant is shown
                    self.assertIn(str.encode(plant.plant_type.name), result.data)    
                else:
                    # We're not assigned, make sure we're not allowed in.
                    self.assert403(result)

    def test_plant_logged_out(self):

        # Check all the plants are there.
        for plant in Plant.query.all():

            # Go to the plant page
            result = self.client.get("/plant/" + str(plant.id))

            # We're not logged in, make sure we're not allowed in.
            self.assert403(result)

    def test_admin_take_taken_job(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/1",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # We shouldn't be allowed to post here, the user is already assigned to this.
        self.assert403(result)

    def test_admin_take_untaken_job(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/2",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # We shouldn't be allowed to post here, the user is already assigned to this.
        self.assert_template_used("plant.html")
        self.assertIn(b'MARK RESOLVED', result.data)

    def test_admin_mark_job_resolved(self):
        self.client.post("/login", 
                        data=dict(email='admin@admin.com', password='admin', remember=False), 
                        follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/2",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # Now try to mark the job as resolved.
        result = self.client.post("/plant/2",
                                    data=dict(submit='MARK RESOLVED'),
                                    follow_redirects=True)

        # The job should now be resolved.
        self.assert_template_used("plant.html")
        self.assertIn(b'TAKE JOB', result.data)


    def test_supervisor_take_taken_job(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/1",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # We shouldn't be allowed to post here, the user is already assigned to this.
        self.assert403(result)

    def test_supervisor_take_untaken_job(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/2",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # We shouldn't be allowed to post here, the user is already assigned to this.
        self.assert_template_used("plant.html")
        self.assertIn(b'MARK RESOLVED', result.data)

    def test_supervisor_mark_job_resolved(self):
        self.client.post("/login", 
                        data=dict(email='supervisor@supervisor.com', password='supervisor', remember=False), 
                        follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/2",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # Now try to mark the job as resolved.
        result = self.client.post("/plant/2",
                                    data=dict(submit='MARK RESOLVED'),
                                    follow_redirects=True)

        # The job should now be resolved.
        self.assert_template_used("plant.html")
        self.assertIn(b'TAKE JOB', result.data)

    def test_user_take_untaken_job(self):
        self.client.post("/login", 
                            data=dict(email='user@user.com', password='user', remember=False), 
                            follow_redirects=True)

        # Try to take the job (notice the post request rather than a get request)
        result = self.client.post("/plant/2",
                                    data=dict(submit='TAKE JOB'),
                                    follow_redirects=True)

        # Make sure it's now taken.
        self.assert_template_used("plant.html")
        self.assertIn(b'MARK RESOLVED', result.data)

    def test_user_mark_resolved(self):
        self.client.post("/login", 
                            data=dict(email='user@user.com', password='user', remember=False), 
                            follow_redirects=True)

        # Try to mark the job as resolved (notice the post request rather than a get request)
        result = self.client.post("/plant/1",
                                    data=dict(submit='MARK RESOLVED'),
                                    follow_redirects=True)

        # Make sure it's now resolved.
        self.assert_template_used("plant.html")
        self.assertIn(b'TAKE JOB', result.data)