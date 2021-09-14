
:: Need to setup environment variables here too - in case we run without setup
call initvars.bat

:: Run the flask application
@echo. && echo Starting application...
flask run --port=5000
