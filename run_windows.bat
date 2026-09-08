@echo off
echo Real Browser Resolution Tester
call venv/Scripts/activate.bat
python src/viewport_sim/viewport_sim.py
exit