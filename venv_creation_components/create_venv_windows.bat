@echo off
echo Creating Python Virtual Environment
cd ..
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install -r ./venv_creation_components/requirements.txt
if errorlevel 1 exit /b 1
python -m playwright install chromium firefox
if errorlevel 1 exit /b 1
echo Venv generation script finished!
exit
