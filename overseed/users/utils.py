import requests, os
from datetime import datetime, timedelta
from flask import flash
from dateutil import tz

INTERVAL_TIME = 15

ERROR_MESSAGES = {
    'temp' : {
        'alert' : {
            'low' : 'Low Temperature!',
            'high' : 'High Temperature!'
        }, 
        'danger' : {
            'low' : 'Extended Low Temperature!',
            'high' : 'Extended High Temperature!'
        }
    },
    'humidity' : {
        'alert' : {
            'low' : 'Low Humidity!',
            'high' : 'High Humidity!' 
        }, 
        'danger' : {
            'low' : 'Extended Low Humidity!',
            'high' : 'Extended High Humidity!'
        }
    }, 
    'moisture' : {
        'alert' : {
            'low' : 'Low Moisture!',
            'high' : 'High Moisture!'
        }, 
        'danger' : {
            'low' : 'Extended Low Moisture!',
            'high' : 'Extended High Moisture!'
        }
    },
    'light' : {
        'alert' : 'Low Light!',
        'danger' : 'Extended Low Light!'
    }
}

EMPTY_ERRORS = {
    'error_level' : 'healthy',
    'error_image' : '',
    'error_messages' : []
}

# This function takes a list of plants, and gets responses from the API for them,
# then runs get_errors on each one and returns a list of errors. 
# ---------------
# Returns a list of errors as long as the list of plants.
def get_plant_list_errors(plants):
    plant_errors = []

    now = datetime.now().astimezone(tz.gettz())

    noAPI = False

    for plant in plants:

        # Check the device exists:
        if plant.device == None:
            plant_errors.append(EMPTY_ERRORS)
        else:
            # For errors, we only need 2 days of data.
            # We use last_days to ensure we get 48 hours of data, no more.
            responses = get_responses(plant.device.hardware_id, now, 2)
            if not responses == "No API":
                responses2 = last_days(responses, now, 2)
                plant_errors.append(get_errors(now, plant.plant_type, responses2))
            else:
                plant_errors.append(EMPTY_ERRORS)
                noAPI = True

    if noAPI:
        flash("The API is not available.", 'danger')

    return plant_errors

# This function takes a given plant type, a set of responses, and a start date.
# ---------------
# Returns a list of errors in the following format:
# Error level -> What level of plant icon to display
# Error icon -> The error icon to display (this will return the highest priority error icon)
# Error messages -> A list of error messages to display.
def get_errors(start, plant_type, responses2):
        
    output = dict()
    output['error_level'] = 'healthy'
    output['error_image'] = None
    output['error_messages'] = []

    if len(responses2) > 0:

        # Check the sensors
        measure_sensor('temp', start, responses2, plant_type, output, 'error_temp_low.png', 'error_temp_high.png')
        measure_sensor('humidity', start, responses2, plant_type, output, 'error_humidity.png', 'error_humidity.png')
        measure_sensor('moisture', start, responses2, plant_type, output, 'error_water.png', 'error_water.png')
        measure_light(responses2, start, plant_type, output)
        measure_connection(responses2, start, output)
    else:
        return None

    # If there are no errors
    if len(output['error_messages']) == 0:
        # Set the error message to blank instead of an array.
        output['error_messages'] = ""

    return output

# This function sends an API request to the API server, for the given device 
# id, start day, and how many days to get.
# ---------------
# Returns a list of responses as provided by the API for the given date range.
def get_responses(device_id, start, how_many_days):

    end = start - timedelta(days=how_many_days)

    try:

        # Get information from the API, using the API_KEY.
        api_key = os.environ['API_KEY']

        r = requests.get(os.environ['API_URL'] + "/api/date/", 
                        { 
                            "api_key": api_key,
                            "device_id": str(device_id), 
                            "start_year": start.year, 
                            "start_month": start.month, 
                            "start_day": start.day, 
                            "end_year": end.year, 
                            "end_month": end.month, 
                            "end_day": end.day 
                        })

        responses = r.json()

        # This sorts the responses by the device_id.
        responses = sorted(responses, key=lambda response: response['id'])

        return responses
    except:
        return "No API"

# This function takes a list of responses.
# ---------------
# Returns a subset of that list of responses that only includes the last X days.
def last_days(responses, start, how_many_days):
    output = []

    for response in reversed(responses):
        response_time = datetime.strptime(response['created_date'], '%a, %d %b %Y %H:%M:%S -0000')

        # Convert the response time (which is in UTC) to AEST so we can compare it to the start time.
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Australia/Melbourne')
        response_time = response_time.replace(tzinfo=from_zone)
        time_in_timezone = response_time.astimezone(to_zone)

        # start - response_time will be how long ago the response was.
        # If we compare that to how_many_days (converted to seconds), we can 
        # determine if we should stop.
        if (start - time_in_timezone).total_seconds() >= how_many_days * 86400:
            pass
        elif (start - time_in_timezone).total_seconds() < 0:
            pass
        else:
            output.append(response)
    
    return output

# This function takes a set of responses, a plant type, and a sensor, and sets up the output 
# according to the values of that sensor in the responses.
# ---------------
# Returns nothing, but edits the output argument.
def measure_sensor(sensor, start, responses2, plant_type, output, low_icon, high_icon):

    min_value = None
    max_value = None
    if sensor == 'temp':
        min_value = plant_type.temperature_low
        max_value = plant_type.temperature_high
    elif sensor == 'humidity':
        min_value = plant_type.humidity_low
        max_value = plant_type.humidity_high
    elif sensor == 'moisture':
        min_value = plant_type.moisture_low
        max_value = plant_type.moisture_high

    assert min_value != None and max_value != None, "Min/Max values not set!"

    i = 0
    time_since_acceptable_value = None
    while time_since_acceptable_value == None and i < len(responses2):
        response = responses2[i]
        value = response[sensor]
    
        # if the value is acceptable, that means we can exit the loop.
        if value >= min_value and value <= max_value:

            # Now calculate how long ago the acceptable range was detected.
            value_time = datetime.strptime(response['created_date'], '%a, %d %b %Y %H:%M:%S -0000').astimezone(tz.gettz('UTC'))

            # Setting the time_since_acceptable_value variable will exit the loop.
            time_since_acceptable_value = (start - value_time).total_seconds()

        i += 1

    # If the loop found an acceptable value:
    if time_since_acceptable_value != None:
        # If it's been 24 hours since an acceptable range, that's danger.
        if time_since_acceptable_value >= 86400:
            increase_error_level(output, 'danger')
            if responses2[0][sensor] < min_value:
                output['error_image'] = low_icon
                output['error_messages'].append(ERROR_MESSAGES[sensor]['danger']['low'])

            if responses2[0][sensor] > max_value:
                output['error_image'] = high_icon
                output['error_messages'].append(ERROR_MESSAGES[sensor]['danger']['high'])
        # Otherwise, there has been an acceptable range within the last 24 hours.
        # Now we check to make sure that it's currently in the acceptable range.
        else:
            if responses2[0][sensor] < min_value:
                increase_error_level(output, 'alert')
                output['error_image'] = low_icon
                output['error_messages'].append(ERROR_MESSAGES[sensor]['alert']['low'])

            if responses2[0][sensor] > max_value:
                increase_error_level(output, 'alert')
                output['error_image'] = high_icon
                output['error_messages'].append(ERROR_MESSAGES[sensor]['alert']['high'])
    # the loop might not get an acceptable value (if, e.g, there are no acceptable 
    # values in the last 24 hours)
    else:
        increase_error_level(output, 'danger')
        if responses2[0][sensor] < min_value:
            output['error_image'] = low_icon
            output['error_messages'].append(ERROR_MESSAGES[sensor]['danger']['low'])

        if responses2[0][sensor] > max_value:
            output['error_image'] = high_icon
            output['error_messages'].append(ERROR_MESSAGES[sensor]['danger']['high'])

# This function takes a set of responses, a plant type, and sets up the output 
# according to the values of the Light sensor in the responses. This has to be different from
# measure_sensor due to the unique way of checking light errors.
# ---------------
# Returns nothing, but edits the output argument.
def measure_light(responses2, start, plant_type, output):

    total_light_minutes_24 = 0
    total_light_minutes_48 = 0
    day_passed = False
    required_light_minutes = plant_type.minimum_light * 60

    for response in responses2:
        if response['light'] == 1:
            if not day_passed:
                total_light_minutes_24 += INTERVAL_TIME
            total_light_minutes_48 += INTERVAL_TIME

        response_time = datetime.strptime(response['created_date'], '%a, %d %b %Y %H:%M:%S -0000').astimezone(tz.gettz('UTC'))

        # If the response was at least 24 hours ago:
        if not day_passed and (start - response_time).total_seconds() >= 86400:
            day_passed = True
        
    if total_light_minutes_24 < required_light_minutes:
        # Now we check if there has been enough light in the last 2 days.
        if total_light_minutes_48 < required_light_minutes * 2:
            increase_error_level(output, 'danger')
            output['error_image'] = 'error_light_low.png'
            output['error_messages'].append(ERROR_MESSAGES['light']['danger'])
        # If we got enough light in the last 48 hours, but didn't in the last 24, that's
        # an alert.
        else:
            increase_error_level(output, 'alert')
            output['error_image'] = 'error_light_low.png'
            output['error_messages'].append(ERROR_MESSAGES['light']['alert'])

# This function takes a set of responses, a start time, and an output argument to edit.
# ---------------
# Returns nothing, but edits the output argument.
def measure_connection(responses2, start, output):

    # Check the Wifi connection.
    last_response = responses2[0]['created_date']
    last_response_time = datetime.strptime(last_response, '%a, %d %b %Y %H:%M:%S -0000').astimezone(tz.gettz('UTC'))

    # How long has it been since that update?
    time_since_update = (start - last_response_time).total_seconds()

    # If at least 24 hours have been missed, that's dangerous
    if time_since_update > 86400:
        increase_error_level(output, 'danger')
        output['error_image'] = 'error_wifi.png'
        output['error_messages'].append("No Wifi connection!")
    # If 12 hours are missed, that's an alert.
    elif time_since_update > 43200:
        increase_error_level(output, 'alert')
        output['error_image'] = 'error_wifi.png'
        output['error_messages'].append("Wifi patchy!")

# This helper function is used to quickly increase the error level.
# ---------------
# Returns nothing, but edits the output argument.
def increase_error_level(output, new_level):

    if output['error_level'] == 'healthy':
        output['error_level'] = new_level
    elif output['error_level'] == 'alert':
        if new_level == 'danger':
            output['error_level'] = new_level
    # If the error level is already danger, then we cannot make changes. Therefore
    # there is no else block.
    