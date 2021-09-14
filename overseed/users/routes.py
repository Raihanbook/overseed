from overseed.users.utils import get_errors, get_responses, get_plant_list_errors, last_days
from overseed import db
from flask import Blueprint, render_template, flash, abort, request
from overseed.models import Plant, RoleID
from overseed.accounts.utils import check_privilege
from flask_login import login_required, current_user
from datetime import datetime
from dateutil import tz

users = Blueprint('users', __name__)

# Plants List
# ---------------
# This page shows all the plants that belong to companies the current user
# is assigned to.
@users.route("/user/plants")
@login_required
def plants_list():
    if not current_user.is_authenticated:
        abort(403)

    if not check_privilege(current_user, RoleID.user.value):
        abort(403)


    companies = current_user.user_assignments
    plants = []

    for company in companies:
        for plant in company.plants:
            plants.append(plant)
    
    plant_errors = get_plant_list_errors(plants)

    return render_template('plants_list.html', title='MY PLANTS', plants=plants, plant_errors=plant_errors, supervisors=False)

# Plant page
# ---------------
# This page shows the data for a given plant. It provides data to the render_template
# function that will be passed into the HTML template file.
# This page also implements a job-taking system.
@users.route("/plant/<string:plantID>", methods=["GET", "POST"])
@login_required
def plant(plantID):
    if not current_user.is_authenticated:
        abort(403)

    current_plant = Plant.query.filter_by(id=plantID).first_or_404()

    assigned_to_plant = False
    for company in current_user.user_assignments:
        if company == current_plant.company:
            assigned_to_plant = True

    if not assigned_to_plant and current_user.privilege_id == RoleID.user.value:
        abort(403)

    device = current_plant.device

    # Variables to hold the data from the API
    responses = []

    # Variables for daily data
    light_daily = []
    moisture_daily = []
    humidity_daily = []
    temp_daily = []
    labels_daily = []

    # Variables for the monthly data
    light_monthly = []
    moisture_monthly = []
    humidity_monthly = []
    temp_monthly = []
    labels_monthly = []

    now = datetime.now().astimezone(tz.gettz())

    responses = []

    error_status = "healthy"
    error_icon = "none"
    errors = ""

    # Get values for the graph
    if device != None:

        responses = get_responses(device.hardware_id, now, 31)

        if not responses == "No API":

            if len(responses) > 0:
                # Variables for the total data of a day worth of data
                a_day_light = 0
                a_day_moist = 0
                a_day_humid = 0
                a_day_temp = 0

                i = 0

                responses_24_hours = last_days(responses, now, 1)

                for plant in reversed(responses_24_hours):
                    # Smooth out the values by only taking 1 in 12.
                    # The calculation makes sure that the most recent value is always 
                    # displayed, by getting every 12 entries starting with the last one.
                    if i % 12 == (len(responses_24_hours)-1) % 12:
                        light_daily.append(plant['light'])
                        moisture_daily.append(plant['moisture'])
                        humidity_daily.append(plant['humidity'])
                        temp_daily.append(plant['temp'])
                        
                        datetime_object = datetime.strptime(plant['created_date'], '%a, %d %b %Y %H:%M:%S -0000')

                        from_zone = tz.gettz('UTC')
                        to_zone = tz.gettz('Australia/Melbourne')

                        datetime_object = datetime_object.replace(tzinfo=from_zone)

                        time_in_timezone = datetime_object.astimezone(to_zone)

                        labels_daily.append(datetime.strftime(time_in_timezone, '%I:%M%p').lstrip("0"))
                    i += 1

                # Var to store how many entries we get from a day worth of data
                data_len = 0
                
                # Var to check whether a day has changed, False at first
                day_changed = False
                
                # Getting the first day in the response, and put it into a var
                str_date = responses[0]['created_date'].split(",")
                prev_day = str_date[0]

                # Monthly data code starts here...
                for plant in responses:
                    # Getting the first day of the responses, and put it into a var
                    str_date = plant['created_date'].split(",")

                    # Check whether the day has changed or not,
                    # if changed, set the day_changed var to True
                    if str_date[0] != prev_day:
                        day_changed = True

                    # Set the previous day with the current data's day
                    prev_day = str_date[0]

                    # If day has changed...
                    if day_changed == True:
                        # Put the average of each data into the monthly vars
                        moisture_monthly.append(round(a_day_moist/data_len))
                        humidity_monthly.append(round(a_day_humid/data_len))
                        temp_monthly.append(round(a_day_temp/data_len))
                        
                        # Calculate light hours of the current plant and put it into the monthly var
                        light_monthly.append(round(a_day_light * 15 / 60))

                        datetime_object = datetime.strptime(plant['created_date'], '%a, %d %b %Y %H:%M:%S -0000')

                        labels_monthly.append(datetime.strftime(datetime_object, '%d %b, %Y'))

                        # Reset the used vars back to original value so they can be used for the next day of data
                        a_day_light = 0
                        a_day_moist = 0
                        a_day_humid = 0
                        a_day_temp = 0
                        data_len = 0
                        day_changed = 0

                        # Taking account of the first entry when a day has changed
                        a_day_moist += plant['moisture']
                        a_day_humid += plant['humidity']
                        a_day_temp += plant['temp']
                        data_len += 1

                        # Count how many times the light data returns 1 and store it to a var
                        if plant['light'] == 1:
                            a_day_light += 1
                    else:
                        # When a day has not changed, run these operations...
                        a_day_moist += plant['moisture']
                        a_day_humid += plant['humidity']
                        a_day_temp += plant['temp']
                        data_len += 1

                        # Count how many times the light data returns 1 and store it to a var
                        if plant['light'] == 1:
                            a_day_light += 1
                
                responses2 = last_days(responses, now, 2)

                output = get_errors(now, current_plant.plant_type, responses2)
                if output != None:
                    error_status = output['error_level']
                    error_icon = output['error_image']
                    errors = output['error_messages']
            else:
                flash("There is no data associated with this plant/device (Hardware ID#" + str(device.hardware_id) + ")", 'danger')
        else:
            flash("The API is not available.", 'danger')
    else:
        flash("There is no device connected to this plant.", 'danger')

    # Check if a method was posted (i.e. the form was submitted)
    if request.method == 'POST':
        if current_user == current_plant.user:
            # This user is already assigned to the plant, so the only 
            # action is to mark it as resolved.

            # We check to make sure reloaded pages won't keep on 
            # marking and taking the job.
            if request.form['submit'] == "MARK RESOLVED":
                current_user.taken_plants.remove(current_plant)
                current_plant.user = None
                db.session.commit()

        elif current_plant.user == None:
            # There is no assigned user. The only action was for the 
            # current user to assign themselves to this plant.
            if request.form['submit'] == "TAKE JOB":
                current_user.taken_plants.append(current_plant)
                current_plant.user = current_user
                db.session.commit()

        else:
            # User exists, but is a different user.
            # If an action has happened, the current user doesn't 
            # have permissions, so we abort and redirect to a 403 
            # error.
            abort(403)

    return render_template('plant.html', plant=current_plant, device=device, 
                            errors=errors, error_status=error_status, error_icon=error_icon,
                            light_daily=light_daily, moisture_daily=moisture_daily,
                            temp_daily=temp_daily, humidity_daily=humidity_daily,
                            labels_daily=labels_daily, light_monthly=light_monthly,
                            moisture_monthly=moisture_monthly, temp_monthly=temp_monthly,
                            humidity_monthly=humidity_monthly, labels_monthly=labels_monthly)
