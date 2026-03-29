@echo off
echo ========================================
echo AI Research Copilot Swarm - Windows
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo.

echo Step 2: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 3: Starting backend server...
echo Backend will run on http://localhost:5000
echo.
echo IMPORTANT: Keep this window open!
echo.
echo To stop the server, press Ctrl+C
echo.
echo ========================================
echo Starting in 3 seconds...
timeout /t 3 /nobreak > nul

cd backend
python app.py
