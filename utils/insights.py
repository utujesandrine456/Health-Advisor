import pandas as pd
import streamlit as st

class DiabetesInsights:
    def __init__(self, data):
        """Initialize with standardized column names and validation"""
        self.data = self._prepare_data(data)
        
    def _prepare_data(self, data):
        """Standardize column names and data format"""
        df = data.copy()
        # Convert all column names to lowercase and handle outcome column
        df.columns = df.columns.str.strip().str.lower()
        
        # Standardize outcome column
        outcome_aliases = ['outcome', 'diabetes', 'target', 'class', 'result']
        for col in df.columns:
            if col.lower() in outcome_aliases:
                df = df.rename(columns={col: 'outcome'})
                break
        
        # Convert numeric columns
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
                
        return df

    def get_diabetes_prevalence(self):
        """Calculate diabetes prevalence with validation"""
        try:
            if 'outcome' not in self.data.columns:
                st.warning("No diabetes outcome column found")
                return 0.0
            return round(self.data['outcome'].mean() * 100, 2)
        except Exception as e:
            st.error(f"Prevalence calculation failed: {str(e)}")
            return 0.0

    def get_average_glucose(self):
        """Get average glucose level for all patients"""
        try:
            if 'glucose' not in self.data.columns:
                st.warning("No glucose data found")
                return 0.0
            return round(self.data['glucose'].mean(), 2)
        except Exception as e:
            st.error(f"Glucose calculation failed: {str(e)}")
            return 0.0

    def get_average_bmi(self):
        """Get average BMI for all patients"""
        try:
            if 'bmi' not in self.data.columns:
                st.warning("No BMI data found")
                return 0.0
            return round(self.data['bmi'].mean(), 2)
        except Exception as e:
            st.error(f"BMI calculation failed: {str(e)}")
            return 0.0

    def get_age_insights(self):
        """Get age-related diabetes insights"""
        result = {
            'high_risk_age_group': 'Data not available',
            'high_risk_percentage': 0,
            'avg_age_diabetes': 0,
            'avg_age_no_diabetes': 0
        }
        
        try:
            if 'age' not in self.data.columns or 'outcome' not in self.data.columns:
                st.warning("Age or outcome data missing")
                return result
            
            diabetic = self.data['outcome'] == 1
            result['avg_age_diabetes'] = round(self.data[diabetic]['age'].mean(), 2)
            result['avg_age_no_diabetes'] = round(self.data[~diabetic]['age'].mean(), 2)
            
            age_groups = pd.cut(
                self.data['age'],
                bins=[0, 30, 45, 60, 100],
                labels=['<30', '30-45', '45-60', '60+']
            )
            
            group_stats = self.data.groupby(age_groups)['outcome'].mean() * 100
            if not group_stats.empty:
                max_group = group_stats.idxmax()
                result.update({
                    'high_risk_age_group': str(max_group),
                    'high_risk_percentage': round(group_stats[max_group], 2)
                })
        except Exception as e:
            st.error(f"Age insight calculation failed: {str(e)}")
            
        return result

    def get_bmi_insights(self):
        """Get BMI-related diabetes insights"""
        result = {
            'high_risk_bmi_category': 'Data not available',
            'high_risk_percentage': 0,
            'avg_bmi_diabetes': 0,
            'avg_bmi_no_diabetes': 0
        }
        
        try:
            if 'bmi' not in self.data.columns or 'outcome' not in self.data.columns:
                st.warning("BMI or outcome data missing")
                return result
            
            diabetic = self.data['outcome'] == 1
            result['avg_bmi_diabetes'] = round(self.data[diabetic]['bmi'].mean(), 2)
            result['avg_bmi_no_diabetes'] = round(self.data[~diabetic]['bmi'].mean(), 2)
            
            bmi_groups = pd.cut(
                self.data['bmi'],
                bins=[0, 18.5, 25, 30, float('inf')],
                labels=['Underweight', 'Normal', 'Overweight', 'Obese']
            )
            
            group_stats = self.data.groupby(bmi_groups)['outcome'].mean() * 100
            if not group_stats.empty:
                max_group = group_stats.idxmax()
                result.update({
                    'high_risk_bmi_category': str(max_group),
                    'high_risk_percentage': round(group_stats[max_group], 2)
                })
        except Exception as e:
            st.error(f"BMI insight calculation failed: {str(e)}")
            
        return result

    def get_glucose_insights(self):
        """Get glucose-related diabetes insights"""
        result = {
            'avg_glucose_diabetes': 0,
            'avg_glucose_no_diabetes': 0,
            'threshold': 126,  # Standard diabetes threshold
            'high_risk_percentage': 0
        }
        
        try:
            if 'glucose' not in self.data.columns or 'outcome' not in self.data.columns:
                st.warning("Glucose or outcome data missing")
                return result
            
            diabetic = self.data['outcome'] == 1
            result['avg_glucose_diabetes'] = round(self.data[diabetic]['glucose'].mean(), 2)
            result['avg_glucose_no_diabetes'] = round(self.data[~diabetic]['glucose'].mean(), 2)
            
            # Calculate risk for high glucose
            high_glucose = self.data['glucose'] > result['threshold']
            result['high_risk_percentage'] = round(self.data[high_glucose]['outcome'].mean() * 100, 2)
            
        except Exception as e:
            st.error(f"Glucose insight calculation failed: {str(e)}")
            
        return result