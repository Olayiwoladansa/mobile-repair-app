@echo off
echo Building IMOSE CRM Desktop Application...
echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt
echo.
echo Step 2: Building executable...
pyinstaller --onefile --windowed --icon=app.ico --name "IMOSE_CRM" main.py
echo.
echo Build complete! Your .exe file is in the 'dist' folder.
echo File: dist\IMOSE_CRM.exe
pause
