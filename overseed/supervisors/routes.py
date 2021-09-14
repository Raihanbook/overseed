from werkzeug.datastructures import CombinedMultiDict
from overseed.users.utils import get_plant_list_errors
from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask.globals import request
from flask_login import login_required, current_user
from overseed.models import Device, Plant, Company, PlantIcon, PlantType, RoleID, User
from overseed.supervisors.forms import CreateDeviceForm, CreatePlantForm, AssignUserForm, CreateCompanyForm
from overseed.supervisors.utils import save_picture
from overseed.accounts.utils import check_privilege
from overseed import supervisors, db

supervisors = Blueprint('supervisors', __name__)

# Plants List
# ---------------
# This page shows all the plants in the system. Admins and Supervisors can add
# plants. Errors are shown dynamically.
@supervisors.route("/plants")
@login_required
def plants_list():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    plants = Plant.query.all()

    plant_errors = get_plant_list_errors(plants)

    return render_template('plants_list.html', title='MANAGE PLANTS', plants=plants, plant_errors=plant_errors, supervisor=True)

# Companies List
# ---------------
# This page shows all the companies in the system. Admins and Supervisors can add 
# and delete companies.
@supervisors.route("/companies")
@login_required
def companies_list():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    companies_normal = Company.query.all()
    companies_ascending = Company.query.order_by(Company.name.asc())
    companies_descending = Company.query.order_by(Company.name.desc())

    supervisor = current_user.privilege_id == RoleID.supervisor.value

    return render_template('companies_list.html', title='MANAGE COMPANIES', companies_normal=companies_normal, 
                            companies_ascending=companies_ascending, companies_descending=companies_descending, supervisor=supervisor)

# Account List
# ---------------
# This page shows all the users in the system. Supervisors can assign users, but 
# cannot add or delete them. Admins can add or delete users.
@supervisors.route("/users")
@login_required
def account_list():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    users = User.query.all()
    
    admin = current_user.privilege_id == RoleID.admin.value

    current_user_id = current_user.id

    return render_template('account_list.html', title='ALL ACCOUNTS', users=users, admin=admin, current_user_id=current_user_id)

# Devices List
# ---------------
# This page shows all the devices in the system. Supervisors can add devices or view 
# existing ones.
@supervisors.route("/devices")
@login_required
def devices_list():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    devices = Device.query.all()
    companies = Company.query.all()

    return render_template('devices_list.html', title='MANAGE DEVICES', devices=devices, companies=companies)

# Create Plant
# ---------------
# This page allows Admins and Supervisors to add a new plant.
@supervisors.route("/create/plant", methods=["GET", "POST"])
@login_required
def create_plant ():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    # Now we create the Create Plant Form.
    form = CreatePlantForm()

    # Some code to turn the array of Companies into an array of strings (names)
    # that starts with a blank entry.
    companies = Company.query.all()
    companiesChoices = [""]
    for company in companies:
        companiesChoices.append(company.name)
    form.company.choices = companiesChoices

    # Same as above, but for types.
    plant_types = PlantType.query.all()
    plantTypeChoices = [""]
    for plant_type in plant_types:
        plantTypeChoices.append(plant_type.name)
    form.type.choices = plantTypeChoices

    # Same as above, but for icons, and there is no blank entry
    icons = PlantIcon.query.all()
    i = 0
    for icon in icons:
        icons[i] = icon.health_1
        i += 1
    form.icon.choices = icons

    # Now we do a check to see if the form has just been submitted to this page.
    if form.validate_on_submit():

        # If we get inside this conditional, it means a valid form has been submitted.
        # Now we create the plant.

        icon = PlantIcon.query.filter_by(health_1 = form.icon.data).first()
        plant_type = PlantType.query.filter_by(name=form.type.data).first()
        company = Company.query.filter_by(name=form.company.data).first()

        newPlant = Plant(icon=icon, plant_type=plant_type, company=company)
        db.session.add(newPlant)
        db.session.commit()

        flash('The new plant has been created.', 'success')

        return redirect(url_for("supervisors.plants_list"))

    return render_template("create_plant.html", title="Create Plant", form=form)

# Assign User
# ---------------
# This page allows Admins and Supervisors to assign a user to a company.
@supervisors.route("/assign_user/<string:user_id>", methods=["GET", "POST"])
@login_required
def assign_user(user_id):
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    # If the curent user has the privilege, load the selected user on the page
    selected_user = User.query.filter_by(id=user_id).first_or_404()

    # If the selected user is Supervisor or Admin, redirect to the Account List Page
    # since you're not allowed to assign these 2 roles to a company
    if check_privilege(selected_user, RoleID.supervisor.value, RoleID.admin.value):
        flash('You cannot assign companies to this account.', 'danger')
        return redirect(url_for('supervisors.account_list'))

    # Load the form
    assign_user_form = AssignUserForm()

    # Get all the companies and add it to the list.
    companies = Company.query.all()
    company_choices = []
    for company in companies:
        company_choices.append(company)
    
    # If there are no choices, users can't assign a user to a company(s).
    if len(company_choices) == 0:
        flash("There are no available companies!", "danger")
        return redirect(url_for("main.home"))

    # Now we set the choices of the companies field.
    assign_user_form.companies.choices = company_choices

    # If the form is valid and submitted
    if assign_user_form.validate_on_submit():

        # Clear all of the assignments in the selected user's field
        selected_user.user_assignments.clear()

        # Assigning the selected user to the selected company(s)
        for result in request.form.getlist('companies'):
            for company in Company.query.all():
                if str(company) == result:
                    company.assigned_to.append(selected_user)
                    db.session.commit()

        # Redirect to the Account List Page, and flash a success message
        flash("Successfully assigned user to the selected companies.", "success")
        return redirect(url_for("supervisors.account_list"))

    return render_template("assign_user.html", title="Assign User " + selected_user.first_name, assign_user_form=assign_user_form, selected_user=selected_user)

# Create device
# ---------------
# This page allows Admins and Supervisors to create a new device.
# This will not be available if there are no available plants without devices.
@supervisors.route("/create/device", methods=["GET", "POST"])
@login_required
def create_device ():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    # Now we create the Create Plant Form.
    form = CreateDeviceForm()
    
    # Get all the plants that don't already have devices.
    plants = Plant.query.all()
    plant_choices = []
    for plant in plants:
        if plant.device == None:
            plant_choices.append(plant)

    # If there are no choices, users can't add devices.
    if len(plant_choices) == 0:
        flash("There are no available plants without devices!", "danger")
        return redirect(url_for("supervisors.devices_list"))

    # Now we set the choices of the plants field.
    form.plant.choices = plant_choices

    # Now we do a check to see if the form has just been submitted to this page.
    if form.validate_on_submit():

        # When passing in the choices to the form macro, the form macro has 
        # to set the values to strings. These strings are python conversions 
        # of the object into a string, so if we compare against the str() 
        # function, they will match if the user has chosen that plant.
        plant = None
        for check_plant in Plant.query.all():
            if str(check_plant) == form.plant.data:
                plant = check_plant

        if plant == None:
            # The chosen plant option does not exist.
            flash("Plant not found!", 'danger')
            return redirect(url_for("supervisors.devices_list"))

        # check if there is a device connected to that plant.
        if plant.device == None:

            new_device = Device(description=form.location.data, hardware_id=form.code.data, plant=plant)
            db.session.add(new_device)

            # There is no connected device, so we connect it here.
            plant.device = new_device

            # The we commit to the database.
            db.session.commit()

            # Flash a success message.
            flash("The device has been created.", 'success')
        else:
            # plant already has a device.
            flash("That plant is already connected to a device! Cancelling device creation...", 'danger')

        return redirect(url_for("supervisors.devices_list"))

    return render_template("create_device.html", title="Create Device", form=form)

# Delete Company
# ---------------
# This page allows Admins and Supervisors to delete companies.
@supervisors.route("/company/delete/<string:company_id>", methods=["GET", "POST"])
@login_required
def delete_company(company_id):
    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.admin.value, RoleID.supervisor.value):
        abort(403)

    # Load the selected company based on the provided ID
    selected_company = Company.query.filter_by(id=company_id).first_or_404()

    # If the company has any plant(s)
    if selected_company.plants != None:
        # Loop through the available company's plant(s) 
        for plant in selected_company.plants:
            # If the current plant has any related device
            if plant.device != None:
                    # First, delete the device related to the current plant
                    db.session.delete(plant.device)
                    # Then, delete the plant itself
                    db.session.delete(plant)
            else:
                # If no related device found, delete just the plant
                db.session.delete(plant)
        # In the end, delete the selected company
        db.session.delete(selected_company)
    else:
        # If the selected company doesn't have any related plant(s), just delete the company
        db.session.delete(selected_company)

    db.session.commit()

    flash('Company has been successfully deleted.', 'success')
    return redirect(url_for("supervisors.companies_list"))
    
# Create Company
# ---------------
# This page allows Admins and Supervisors to create new companies.
@supervisors.route("/create/company", methods=["GET", "POST"])
@login_required
def create_company ():
    if not current_user.is_authenticated:
        abort(403)

    # Check if the user's role is NOT in the specified roles to access the page
    # See utils.py file in the accounts folder for the function
    if not check_privilege(current_user, RoleID.supervisor.value, RoleID.admin.value):
        abort(403)

    # Now we create the Create Company Form.
    form = CreateCompanyForm(CombinedMultiDict((request.files, request.form)))

    # Now we do a check to see if the form has just been submitted to this page.
    if form.validate_on_submit():

        if form.icon.data:
            company_icon = save_picture(form.icon.data)

        # creating a new company and adding it to the session.
        new_company = Company(name=form.name.data, 
                            icon=company_icon, 
                            phone_number=form.phone_number.data, 
                            contact_email=form.contact_email.data, 
                            contact_name=form.contact_name.data, 
                            address=form.address.data, 
                            notes=form.notes.data,
                            active=1)
        
        db.session.add(new_company)

        # The we commit to the database.
        db.session.commit()

        # Flash a success message.
        flash("The company has been created.", 'success')

        return redirect(url_for("supervisors.companies_list"))

    return render_template("create_company.html", title="Create Company", form=form)
