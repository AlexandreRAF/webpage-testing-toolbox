@echo off
echo Real Browser Resolution Tester
cd ..
cd ..
call venv/Scripts/activate.bat
python src/viewport_sim/viewport_sim.py
exit