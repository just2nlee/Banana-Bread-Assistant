@echo off
echo Starting BananaPredictor API...
cd /d %~dp0
call ..\venv\Scripts\activate.bat
python main.py
pause

