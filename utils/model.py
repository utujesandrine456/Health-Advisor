import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os


class DiabetesPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_columns = [
            'pregnancies', 'glucose', 'bloodpressure',
            'skinthickness', 'insulin', 'bmi',
            'diabetespedigreefunction', 'age'
        ]
        self.is_trained = False
        self.model_path = "models/diabetes_model.pkl"
        self.scaler_path = "models/scaler.pkl"

    def _prepare_data(self, data):
        """Standardize and validate input data"""
        data = data.copy()
        data.columns = data.columns.str.lower()
        
        # Check for required columns
        missing_cols = [col for col in self.feature_columns 
                       if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        if 'outcome' not in data.columns:
            raise ValueError("Missing 'outcome' column in training data")
            
        return data

    def train_model(self, data):
        """Complete training workflow with evaluation"""
        try:
            data = self._prepare_data(data)
            
            # Prepare features and target
            X = data[self.feature_columns]
            y = data['outcome']
            
            # Handle missing values
            X = X.fillna(X.median())
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            self.scaler.fit(X_train)
            X_train_scaled = self.scaler.transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            with st.spinner("Training model..."):
                self.model.fit(X_train_scaled, y_train)
                self.is_trained = True
                
                # Save model and scaler
                os.makedirs("models", exist_ok=True)
                joblib.dump(self.model, self.model_path)
                joblib.dump(self.scaler, self.scaler_path)
            
            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Display results
            st.success("✅ Model trained successfully!")
            st.metric("Test Accuracy", f"{accuracy:.1%}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Classification Report")
                st.text(classification_report(y_test, y_pred))
            
            with col2:
                st.subheader("Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                st.write(pd.DataFrame(cm, 
                    columns=['Predicted 0', 'Predicted 1'],
                    index=['Actual 0', 'Actual 1']))
            
            return True
            
        except Exception as e:
            st.error(f"Training failed: {str(e)}")
            self.is_trained = False
            return False

    def load_model(self):
        """Load pre-trained model from disk"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                return True
            return False
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            return False

def train_model(df, features, target):
    """Train a machine learning model and return model, score, and report"""
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score, mean_squared_error
        import numpy as np
        
        # Prepare data
        X = df[features].fillna(df[features].median())
        y = df[target].fillna(df[target].median())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        score = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        # Create report
        report = f"""
        Model Performance Report:
        ========================
        Target Variable: {target}
        Features Used: {', '.join(features)}
        R² Score: {score:.3f}
        Mean Squared Error: {mse:.3f}
        Root Mean Squared Error: {rmse:.3f}
        
        Feature Importance:
        ==================
        """
        
        # Add feature importance
        feature_importance = pd.DataFrame({
            'Feature': features,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        for _, row in feature_importance.iterrows():
            report += f"{row['Feature']}: {row['Importance']:.3f}\n"
        
        return model, score, report
        
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return None, 0.0, f"Error: {str(e)}"

def load_model(model_path):
    """Load a trained model from file"""
    try:
        import joblib
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None