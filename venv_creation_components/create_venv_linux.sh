echo Creating Python Virtual Environment
python3 -m venv ../venv
source ../venv/bin/activate
python -m pip install -r ./requirements.txt && python -m playwright install chromium firefox
