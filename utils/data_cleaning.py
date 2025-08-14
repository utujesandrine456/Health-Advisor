import pandas as pd
import numpy as np

class DataCleaner:
    """Class for advanced data cleaning operations"""
    
    def clean_data(self, df):
        """Complete cleaning pipeline with validation"""
        # Standardize column names first
        df.columns = df.columns.str.lower()
        
        # Handle outcome column
        outcome_cols = [col for col in df.columns if col in ['outcome', 'diabetes', 'target']]
        if outcome_cols:
            df = df.rename(columns={outcome_cols[0]: 'outcome'})
        
        # Rest of your cleaning steps...
        
        # Final validation
        if 'outcome' not in df.columns:
            st.warning("No outcome column found after cleaning")
            
        return df


    def __init__(self):
        self.numeric_columns = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]
        
        # Define valid ranges for each numeric column
        self.valid_ranges = {
            'Pregnancies': (0, 25),
            'Glucose': (0, 300),
            'BloodPressure': (0, 200),
            'SkinThickness': (0, 100),
            'Insulin': (0, 1000),
            'BMI': (10, 100),
            'DiabetesPedigreeFunction': (0, 5),
            'Age': (0, 120)
        }
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        df = df.copy()  # Create a copy to avoid modifying the original
        
        # Convert numeric columns to float and handle outliers
        for col in self.numeric_columns:
            if col in df.columns:
                # Replace invalid values with NaN
                df[col] = df[col].replace({
                    '-': np.nan,
                    'N/A': np.nan,
                    'NA': np.nan,
                    'na': np.nan,
                    'NULL': np.nan,
                    'null': np.nan,
                    '?': np.nan,
                    '': np.nan
                })
                
                # Convert to numeric, forcing errors to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Handle outliers based on valid ranges
                min_val, max_val = self.valid_ranges[col]
                df[col] = df[col].clip(lower=min_val, upper=max_val)
                
                # Replace remaining NaN values with median
                median_value = df[col][(df[col] >= min_val) & (df[col] <= max_val)].median()
                df[col] = df[col].fillna(median_value)
        
        return df
    
    def remove_duplicates(self, df):
        """Remove duplicate rows from the dataset"""
        df.drop_duplicates(inplace=True)
        return df
    
    def handle_outliers(self, df):
        """Handle outliers using IQR method"""
        for col in df.select_dtypes(include=['float64', 'int64']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
            df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
            
        return df
    
    def feature_engineering(self, df):
        """Create new features from existing data"""
        df = df.copy()  # Create a copy to avoid modifying the original dataframe
        
        # Ensure all numeric columns are properly typed
        numeric_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                         'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
        for col in numeric_columns:
            if col in df.columns:
               
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                if df[col].isnull().any():
                    df[col].fillna(df[col].median(), inplace=True)
        
        
        if 'BMI' in df.columns and pd.api.types.is_numeric_dtype(df['BMI']):
            
            df['BMI'] = pd.to_numeric(df['BMI'], errors='coerce')
            df['BMI'] = df['BMI'].clip(lower=0)
            df['BMI'].fillna(df['BMI'].median(), inplace=True)
            
            df['BMI_Category'] = pd.cut(
                df['BMI'],
                bins=[-float('inf'), 18.5, 25, 30, float('inf')],
                labels=['Underweight', 'Normal', 'Overweight', 'Obese']
            )
        
        
        if 'Age' in df.columns and pd.api.types.is_numeric_dtype(df['Age']):
            
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            df['Age'] = df['Age'].clip(lower=0)
            df['Age'].fillna(df['Age'].median(), inplace=True)
            
            df['Age_Group'] = pd.cut(
                df['Age'],
                bins=[-float('inf'), 30, 45, 60, float('inf')],
                labels=['Young', 'Adult', 'Senior', 'Elderly']
            )
        
        return df
    


    def standardize_column_names(self, df):
        """Standardize all column names, especially the outcome column"""
        df.columns = df.columns.str.lower()  # Convert all to lowercase
        
        # Handle common variations of the outcome column
        outcome_aliases = ['outcome', 'diabetes', 'target', 'result']
        for alias in outcome_aliases:
            if alias in df.columns:
                df = df.rename(columns={alias: 'outcome'})
                break
                
        return df


class AdvancedDataCleaner:
    """Advanced data cleaning class with comprehensive features for the health advisor app"""
    
    def __init__(self):
        """Initialize the advanced data cleaner"""
        pass
    
    def comprehensive_data_cleaning(self, uploaded_file):
        """Perform comprehensive data cleaning on uploaded file"""
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            
            # Basic cleaning
            df = self._basic_cleaning(df)
            
            # Handle missing values
            df = self._handle_missing_values(df)
            
            # Remove duplicates
            df = self._remove_duplicates(df)
            
            # Standardize column names
            df = self._standardize_columns(df)
            
            # Handle outliers
            df = self._handle_outliers(df)
            
            return df
            
        except Exception as e:
            st.error(f"Error during data cleaning: {str(e)}")
            return None
    
    def _basic_cleaning(self, df):
        """Perform basic data cleaning"""
        # Remove leading/trailing whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Convert empty strings to NaN
        df = df.replace(['', 'nan', 'NaN', 'NULL', 'null'], np.nan)
        
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values intelligently"""
        # For numerical columns, fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                df[col] = df[col].fillna(mode_val)
        
        return df
    
    def _remove_duplicates(self, df):
        """Remove duplicate rows"""
        initial_rows = len(df)
        df = df.drop_duplicates()
        removed_rows = initial_rows - len(df)
        
        if removed_rows > 0:
            st.info(f"Removed {removed_rows} duplicate rows")
        
        return df
    
    def _standardize_columns(self, df):
        """Standardize column names"""
        # Convert to lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        
        return df
    
    def _handle_outliers(self, df):
        """Handle outliers using IQR method"""
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing them
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        return df
    