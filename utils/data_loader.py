# utils/data_loader.py
import pandas as pd
import streamlit as st

def load_data():
    """Load data with robust column name handling"""
    try:
        df = pd.read_csv("data/diabetes_messy.csv")
        
        # Standardize column names
        df.columns = df.columns.str.strip().str.lower()
        
        # Handle common outcome column names
        outcome_aliases = ['outcome', 'diabetes', 'target', 'class', 'result']
        for alias in outcome_aliases:
            if alias in df.columns:
                df = df.rename(columns={alias: 'outcome'})
                break
                
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()