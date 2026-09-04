@echo off
echo Creating Python Virtual Environment
cd ..
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install -r ./venv_creation_components/requirements.txt
echo Venv generation script finished!
exit