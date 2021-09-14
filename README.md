# Overseed
This project is the front end for the Smart Plant IoT project.

These instrunctions are for developers (on windows) - for more details please read
"#24 - Installation Instructions.docx"

# Deployment

Currently, any merge to staging will cause an automatic deployment to the website.
This is available through https://overseed-staging.herokuapp.com

In order to deploy to main - the process must be manually completed (to avoid accidental deploys)

# How to install

Create the repo locally and cd into the directory:

$ git clone https://github.com/s3387728/Overseed.git

$ cd Overseed

If this is the first time pulling the code, you need to create a virtual environment.

$ python -m venv .venv
$ .\.venv\Scripts\activate.bat

If you are pulling new code, that may have new packages installed, or you have just created
your virtual environment, then you need to install all the dependencies:

$ pip install -r requirements.txt

# Add the database

Assuming the database has not been created before - you will need to setup the database and some test data.

$ ./setupdatabase.bat

This script is a simple batch script that will set the required environment variables, and 
run the flask project:

$ ./startup.bat

At this point the webserver should be running, and flask should print the IP address that you can
access the site at as the last line of the output

# Adding a new dependency

Make sure you have your virtual environment active. You can then add new dependencies, and it will
be copied into the virtual environment folder. This is important as the dependencies in this folder are the ones that are written to requirements.txt

$ pip install package_name

# How to update your requirements.txt file

You only need to do this if you have added a new dependency, or if you have upgraded a version. In general, we will not change this file that much once the project is setup, unless we are adding
a new feature. 

$ pip freeze > requirements.txt

# Python version

Please use a recent version of Python (3.9 or later) - If you get a warning about your pip version, you may ignore that.

# Deployment

The project will be hosted on Heroku (at this stage)
We will use branches to push code - so "main" will be the stable branch we push from
(It is okay to push to main directly for now - but we will change this)
(Please note: it is no longer appropriate to have "master" branches in GitHub - hence "main")

# Passwords

email: admin@admin.com
password: admin

email: supervisor@supervisor.com
password: supervisor

email: user@user.com
password: user
