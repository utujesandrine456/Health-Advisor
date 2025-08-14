#!/usr/bin/env python3
"""
Health Tracker Application Launcher
A premium health analytics and machine learning platform
"""

import streamlit as st
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def main():
    """Launch the Health Tracker application"""
    try:
        # Import and run the main app
        from main_app import create_premium_app
        create_premium_app()
    except Exception as e:
        st.error(f"Error launching application: {str(e)}")
        st.info("Please make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()

