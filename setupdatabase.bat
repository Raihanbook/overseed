::creating the database

:: Because this will be run in a separate instance, we need to duplicate these
:: environment variables
:: And make sure we are running in the virtual environment

CALL %0\..\venv\Scripts\activate.bat

CALL initvars.bat

echo "importing initial data"
py db_create.py
