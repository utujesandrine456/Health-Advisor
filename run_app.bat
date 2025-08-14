@echo off
echo ========================================
echo    Health Tracker - Premium Analytics
echo ========================================
echo.
echo Starting Health Tracker Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the application
echo.
echo Launching Health Tracker...
echo The application will open in your default browser
echo Press Ctrl+C to stop the application
echo.
streamlit run app/main_app.py

pause

