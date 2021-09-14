
# Readme for the overseed application

Please note, that this readme.txt is different to the README.MD file due to different requirements and
the need to separate the information in these two files.

# Github URL
https://github.com/s3387728/Overseed

# Deployed URL (on Heroku)
https://www.overseed.xyz/

# Test user accounts
- We have provided two user accounts that can be used to access Heroku and git
-- Heroku: overseedtestuser1@gmail.com / overseed060621!
-- Heroku: overseedtestuser2@gmail.com / overseed060621!
-- Github: overseedtestuser1@gmail.com / overseed060621
-- Github: overseedtestuser2@gmail.com / overseed060621
- If required, you can access the gmail email accounts with the following credentials
-- Gmail: overseedtestuser1@gmail.com / overseed060621
-- Gmail: overseedtestuser2@gmail.com / overseed060621

# Installation (windows / mac / linux)
For detailed instructions see the accomponying installation document.
- Ensure you have at least python 3.6 (3.9 is preferred)
- Make sure you have pip and virtualenv installed

There are three main steps that need to be performed when installing and running the app
1. Install the overseed app
2. Install the overseed API service
3. Initialise and populate the API database

This document covers installing the overseed app to a local windows machine (step 1)

# Installing for the first time
- To install the overseed app - go to the Overseed directory and run:
windows:    install.bat
Linux/Mac:  source install.sh

- To install and create the initial database
Windows: setupdatabase.bat
Linux/Mac: source setupdatabase.sh

- If this succeeds run 
Windows:   startup.bat
Linux/Mac:     startup.sh 

You can verify the server is running by navigating to:
http:/127.0.0.1:5000

NOTE: You will require the API service to be running to actually use the app, follow the instructions there

# Subsequent runs (i.e. database has been installed and the environment is installed)
If you cannot see "venv" on your command prompt, you may need to start the virtual environment
- On windows run: venv/Scripts/activate.bat
- On Linux/Mac run: source venv/bin/activate
- To start the actual application:
- On windows run: startup.bat
- On mac/linux run: startup.show

# Known Issues / outstanding bugs

- The application is currently only using a hard coded API key for authentication this could be improved in the next version
- Company deletion doesn't clear out our device setup properly. 
- Heroku does not support static image uploads (as the file system is transient), this means uploaded images (for companies etc) may disappear the next time the server restarts (daily)
- Back button will not always work in some pages
