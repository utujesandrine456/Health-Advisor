#!/bin/bash

echo "========================================"
echo "   Health Tracker - Premium Analytics"
echo "========================================"
echo ""
echo "Starting Health Tracker Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip3 show streamlit &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Run the application
echo ""
echo "Launching Health Tracker..."
echo "The application will open in your default browser"
echo "Press Ctrl+C to stop the application"
echo ""
streamlit run app/main_app.py

