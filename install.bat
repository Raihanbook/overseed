@echo. && echo Installing Overseed application... 

@echo Setting up virtual environment...
py -m venv venv
::cmd.exe /c ".\venv\Scripts\activate.bat"
CALL %0\..\venv\Scripts\activate.bat

@echo Installing packages...
pip install -r requirements.txt

call initvars.bat

@echo. && echo Installation complete.
@echo. && echo Execute "startup.bat" to begin application.
@echo off
pause
