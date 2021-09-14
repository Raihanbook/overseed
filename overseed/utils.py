from overseed import db, bcrypt
from overseed.models import Privilege, User, PlantIcon, Plant, Company, Device, PlantType

# This function resets the database with dummy data.
# ---------------
# Returns nothing, but edits the overseed package's db database.
def delete_and_create_db():
    
    db.drop_all()
    db.create_all()

    admin = Privilege(name='admin', notes='admin')
    supervisor = Privilege(name='supervisor', notes='supervisor')
    user = Privilege(name='user', notes='user')

    db.session.add(admin)
    db.session.add(supervisor)
    db.session.add(user)

    hashed_password_admin = bcrypt.generate_password_hash('admin').decode('utf-8')
    hashed_password_supervisor = bcrypt.generate_password_hash('supervisor').decode('utf-8')
    hashed_password_user = bcrypt.generate_password_hash('user').decode('utf-8')

    user_admin = User(first_name='admin', last_name='admin', email='admin@admin.com', password=hashed_password_admin, privilege=admin, active=1)
    user_supervisor = User(first_name='supervisor', last_name='supervisor', email='supervisor@supervisor.com', password=hashed_password_supervisor, privilege=supervisor, active=1)
    user_user = User(first_name='user', last_name='user', email='user@user.com', password=hashed_password_user, privilege=user, active=1)

    db.session.add(user_admin)
    db.session.add(user_supervisor)
    db.session.add(user_user)

    aloeIcon = PlantIcon(health_1="aloe_healthy.png", health_2="aloe_alert.png", health_3="aloe_danger.png")
    bonsaiIcon = PlantIcon(health_1="bonsai_healthy.png", health_2="bonsai_alert.png", health_3="bonsai_danger.png")
    pricklyPearIcon = PlantIcon(health_1="prickly_pear_healthy.png", health_2="prickly_pear_alert.png", health_3="prickly_pear_danger.png")
    leavesIcon = PlantIcon(health_1="leaves_healthy.png", health_2="leaves_alert.png", health_3="leaves_danger.png")
    bushIcon = PlantIcon(health_1="bush_healthy.png", health_2="bush_alert.png", health_3="bush_danger.png")
    treeIcon = PlantIcon(health_1="tree_healthy.png", health_2="tree_alert.png", health_3="tree_danger.png")
    pileaIcon = PlantIcon(health_1="pilea_healthy.png", health_2="pilea_alert.png", health_3="pilea_danger.png")
    cactusIcon = PlantIcon(health_1="cactus_healthy.png", health_2="cactus_alert.png", health_3="cactus_danger.png")

    db.session.add(bushIcon)
    db.session.add(treeIcon)
    db.session.add(pileaIcon)
    db.session.add(cactusIcon)
    db.session.add(aloeIcon)
    db.session.add(bonsaiIcon)
    db.session.add(pricklyPearIcon)
    db.session.add(leavesIcon)

    companyX = Company(name="Company X", phone_number="0432 123 456", address="123 Good Rd. Melboure, 3004, Australia", icon="company_x.png", active=1)
    companyY = Company(name="Y Inc.", phone_number="0432 123 456", address="123 Good Rd. Melboure, 3004, Australia", icon="company_y.png", active=1)
    companyZ = Company(name="Z and A Law Firm", phone_number="0432 123 456", address="123 Good Rd. Melboure, 3004, Australia", icon="company_z.png", active=1)

    db.session.add(companyX)
    db.session.add(companyY)
    db.session.add(companyZ)

    device_1 = Device(description="Entrance window", hardware_id="1100")
    device_2 = Device(description="Reception Countertop", hardware_id="1200")

    # High/Low Humidity Alert at some points during the day.
    aloeVera = PlantType(name="Aloe Vera", description="A small succulent, known for its ability to heal burned skin.", care_instructions="Does not need much water.", \
        humidity_high=40, humidity_low=30, \
            temperature_high=100, temperature_low=0, \
                moisture_high=100, moisture_low=0, \
                    minimum_light=1)

    # High/Low Temperature Alert at some points during the day
    pricklyPear = PlantType(name="Prickly Pear", description="The fruit of prickly pear (erect) has reddish-purple skin, reddish flesh and is somewhat pear-shaped. The fruit grows to 4 to 6cm long and bears tufts of fine barbed bristles in areoles.", care_instructions="Prickly pears are extremely drought tolerant. Don't water newly propagated pads for the first month. After that, water every two to four weeks for the first year — twice a month in summer and once a month other times of the year. In most areas, rainfall will be enough to sustain established plants.", \
        humidity_high=100, humidity_low=0, \
            temperature_high=20, temperature_low=17, \
                moisture_high=100, moisture_low=0, \
                    minimum_light=1)

    # High Moisture Danger
    peaceLily = PlantType(name="Peace Lily", description="Peace lilies are sturdy plants with glossy, dark green oval leaves that narrow to a point. The leaves rise directly from the soil. These plants also periodically produce lightly fragrant white flowers that resemble calla lilies. The long-lasting flowers start out pale green and slowly turn creamy white as they open.", care_instructions="Place plants in bright, indirect light. Keep the soil consistently moist but not soggy.", \
        humidity_high=100, humidity_low=0, \
            temperature_high=100, temperature_low=0, \
                moisture_high=30, moisture_low=21, \
                    minimum_light=1)

    # No Errors
    snakePlant = PlantType(name="Snake Plant", description="Snake Plants are evergreen perennials that can grow anywhere from eight inches to 12 feet high. Their sword-like leaves are approximately two feet long. The foliage is stiff, broad, and upright, in a dark green color variegated with white and yellow striping.", care_instructions="Snake plants prefer bright, indirect light and can even tolerate some direct sunlight. However, they also grow well (albeit more slowly) in shady corners and other low-light areas of the home. Keep the plant in a warm spot with temperatures above 50°F (10°C). In the winter, be sure to protect it from drafty windows.", \
        humidity_high=50, humidity_low=30, \
            temperature_high=100, temperature_low=0, \
                moisture_high=100, moisture_low=0, \
                    minimum_light=1)

    # Low Light Danger
    spiderPlant = PlantType(name="Spider Plant", description="Spider Plant is an evergreen, perennial plant with tuberous roots and tuft appearance. At height and diameter it does not exceed 50 cm, but it can be spread on the ground and cover a considerable area. Its foliage is of medium density, and has a fine texture.", care_instructions="Spider plant likes a moist soil or potting mix that drains well, but it can also tolerate periods of dryness. Don't over-water or the roots may rot. As long as it's given an application of controlled-release fertiliser once a year at the start of spring, your spider plant will be happy.", \
        humidity_high=100, humidity_low=0, \
            temperature_high=100, temperature_low=0, \
                moisture_high=100, moisture_low=0, \
                    minimum_light=14)

    plant_0 = Plant(device=device_1, icon=aloeIcon, plant_type=aloeVera, company=companyX, user=user_user)
    plant_1 = Plant(device=device_2, icon=pricklyPearIcon, plant_type=pricklyPear, company=companyX)
    plant_2 = Plant(device=device_1, icon=bushIcon, plant_type=peaceLily, company=companyY)
    plant_3 = Plant(device=device_2, icon=aloeIcon, plant_type=snakePlant, company=companyY)
    plant_4 = Plant(device=device_1, icon=leavesIcon, plant_type=spiderPlant, company=companyZ)

    db.session.add(device_1)
    db.session.add(device_2)

    db.session.add(aloeVera)
    db.session.add(pricklyPear)
    db.session.add(peaceLily)
    db.session.add(snakePlant)
    db.session.add(spiderPlant)

    db.session.add(plant_0)
    db.session.add(plant_1)
    db.session.add(plant_2)
    db.session.add(plant_3)
    db.session.add(plant_4)

    companyX.assigned_to.append(user_user)
    companyY.assigned_to.append(user_user)

    db.session.commit()