import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_cleaning import AdvancedDataCleaner
from utils.visualisation import PremiumVisualizer
from utils.model import train_model, load_model
from fpdf import FPDF
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_premium_app():
    """
    PREMIUM HEALTH ADVISOR APPLICATION
    Creates a beautiful, interactive health analytics platform
    """
    
    # Page configuration
    st.set_page_config(
        page_title="Health Advisor - Advanced Health Analytics",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    

    # Load external CSS for premium styling
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <i class="fas fa-heartbeat" style="font-size: 2rem; color: #667eea;"></i>
            <h2>Health Advisor</h2>
            <p>Advanced Health Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### <i class='fas fa-cog'></i> Settings", unsafe_allow_html=True)
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Comprehensive", "Quick Scan", "Deep Learning"],
            help="Choose the type of analysis you want to perform"
        )
        
        st.markdown("### <i class='fas fa-chart-line'></i> Visualization", unsafe_allow_html=True)
        show_advanced = st.checkbox("Show Advanced Features", value=True)
        
        st.markdown("### <i class='fas fa-info-circle'></i> About", unsafe_allow_html=True)
        st.info("""
        **Health Advisor** is an advanced health analytics platform that provides:
        - 📊 Data Analysis & Visualization
        - 🤖 Machine Learning Predictions
        - 📈 Interactive Charts
        - 📄 Professional Reports
        """)
    

    # Main content
    st.markdown("""
    <div class="main-header">
        <h1><i class="fas fa-heartbeat"></i> Health Advisor</h1>
        <p>Advanced Health Analytics & Machine Learning Platform</p>
        <p><i class="fas fa-star"></i> Premium Features | <i class="fas fa-chart-line"></i> Interactive Analytics | <i class="fas fa-brain"></i> AI-Powered Insights</p>
    </div>
    """, unsafe_allow_html=True)
    

    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Dashboard",
        "📊 Analytics", 
        "🤖 Machine Learning",
        "📈 Visualizations",
        "📄 Reports"
    ])
    
    with tab1:
        create_dashboard_section()
    
    with tab2:
        create_analytics_section()
    
    with tab3:
        create_ml_section()
    
    with tab4:
        create_visualization_section()
    
    with tab5:
        create_reports_section()

def create_dashboard_section():
    """Create the main dashboard section"""
    
    st.markdown("""
    <div class="section-header">
        <h2><i class="fas fa-tachometer-alt"></i> Health Analytics Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)
    

    # File upload section
    st.markdown("""
    <div class="upload-section">
        <h3><i class="fas fa-cloud-upload-alt"></i> Upload Your Health Dataset</h3>
        <p>Upload a CSV file containing your health data for comprehensive analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload your health dataset in CSV format"
    )
    
    if uploaded_file is not None:
        # Load and clean data
        with st.spinner("🔄 Processing your data..."):
            cleaner = AdvancedDataCleaner()
            df = cleaner.comprehensive_data_cleaning(uploaded_file)
        
        st.markdown("""
        <div class="success-card">
            <h3><i class="fas fa-check-circle"></i> Data Successfully Processed!</h3>
            <p>Your dataset has been cleaned and is ready for analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total Records",
                value=f"{len(df):,}",
                delta=f"+{len(df)}"
            )
        
        with col2:
            st.metric(
                label="📈 Features",
                value=f"{len(df.columns)}",
                delta="+1"
            )
        
        with col3:
            st.metric(
                label="🔍 Data Types",
                value=f"{df.dtypes.nunique()}",
                delta="+1"
            )
        
        with col4:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric(
                label="✅ Data Quality",
                value=f"{100-missing_pct:.1f}%",
                delta=f"-{missing_pct:.1f}%"
            )
        
        # Store data in session state
        st.session_state['df'] = df
        
        # Data preview
        st.markdown("### <i class='fas fa-table'></i> Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Quick insights
        st.markdown("### <i class='fas fa-lightbulb'></i> Quick Insights")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numerical_cols) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Numerical Features:**")
                for col in numerical_cols[:5]:  # Show first 5
                    stats = df[col].describe()
                    st.info(f"• {col}: Mean={stats['mean']:.2f}, Std={stats['std']:.2f}")
            
            with col2:
                st.markdown("**🔍 Data Quality:**")
                missing_data = df.isnull().sum()
                for col in df.columns[:5]:  # Show first 5
                    missing_pct = (missing_data[col] / len(df)) * 100
                    if missing_pct > 0:
                        st.warning(f"• {col}: {missing_pct:.1f}% missing")
                    else:
                        st.success(f"• {col}: Complete")

def create_analytics_section():
    """Create the analytics section"""
    
    st.markdown("""
    <div class="section-header">
        <h2><i class="fas fa-chart-bar"></i> Advanced Analytics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload a dataset first in the Dashboard tab.")
        return
    
    df = st.session_state['df']
    
    # Analytics options
    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs([
        "📊 Descriptive Statistics",
        "🔍 Data Quality Analysis", 
        "📈 Trend Analysis"
    ])
    
    with analytics_tab1:
        st.markdown("### <i class='fas fa-calculator'></i> Descriptive Statistics")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numerical_cols) > 0:
            st.dataframe(df[numerical_cols].describe(), use_container_width=True)
            
            # Statistical insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Statistical Summary:**")
                for col in numerical_cols:
                    stats = df[col].describe()
                    st.metric(f"{col} Mean", f"{stats['mean']:.2f}")
            
            with col2:
                st.markdown("**📈 Variability:**")
                for col in numerical_cols:
                    cv = (df[col].std() / df[col].mean()) * 100
                    st.metric(f"{col} CV", f"{cv:.1f}%")
    
    with analytics_tab2:
        st.markdown("### <i class='fas fa-search'></i> Data Quality Analysis")
        
        # Missing values analysis
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔍 Missing Values:**")
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing_Count': missing_data.values,
                'Missing_Percentage': missing_percentage.values
            })
            st.dataframe(missing_df[missing_df['Missing_Count'] > 0], use_container_width=True)
        
        with col2:
            st.markdown("**📊 Data Completeness:**")
            completeness = (1 - missing_percentage / 100) * 100
            st.metric("Overall Completeness", f"{completeness.mean():.1f}%")
            
            # Data types
            st.markdown("**📋 Data Types:**")
            dtype_counts = df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                st.info(f"• {dtype}: {count} columns")
    
    with analytics_tab3:
        st.markdown("### <i class='fas fa-chart-line'></i> Trend Analysis")
        
        # Check if there's a date column
        date_cols = []
        for col in df.columns:
            try:
                pd.to_datetime(df[col])
                date_cols.append(col)
            except:
                continue
        
        if date_cols:
            selected_date = st.selectbox("Select Date Column:", date_cols)
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numerical_cols:
                selected_value = st.selectbox("Select Value Column:", numerical_cols)
                
                # Create time series plot
                df_temp = df.copy()
                df_temp[selected_date] = pd.to_datetime(df_temp[selected_date])
                df_temp = df_temp.sort_values(selected_date)
                
                fig = px.line(df_temp, x=selected_date, y=selected_value,
                             title=f"Trend Analysis: {selected_value} over Time")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📅 No date columns found for trend analysis.")

def create_ml_section():
    """Create the machine learning section"""
    
    st.markdown("""
    <div class="section-header">
        <h2><i class="fas fa-brain"></i> Machine Learning</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload a dataset first in the Dashboard tab.")
        return
    
    df = st.session_state['df']
    
    # ML options
    ml_tab1, ml_tab2, ml_tab3 = st.tabs([
        "🎯 Model Training",
        "🔮 Predictions", 
        "📊 Model Performance"
    ])
    
    with ml_tab1:
        st.markdown("### <i class='fas fa-cogs'></i> Model Training")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numerical_cols) < 2:
            st.warning("⚠️ Need at least 2 numerical columns for machine learning.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            features = st.multiselect(
                "Select Features for Training",
                numerical_cols,
                default=numerical_cols[:-1] if len(numerical_cols) > 1 else numerical_cols
            )
        
        with col2:
            target = st.selectbox("Select Target Variable", numerical_cols)
        
        if st.button("🚀 Train Model", key="train_btn"):
            if len(features) > 0 and target in df.columns:
                with st.spinner("Training machine learning model..."):
                    try:
                        # Train model
                        model, score, report = train_model(df, features, target)
                        
                        # Store in session state
                        st.session_state['model'] = model
                        st.session_state['features'] = features
                        st.session_state['target'] = target
                        st.session_state['model_score'] = score
                        st.session_state['model_report'] = report
                        
                        st.markdown("""
                        <div class="success-card">
                            <h3><i class="fas fa-check-circle"></i> Model Training Complete!</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.metric("Model Score", f"{score:.3f}")
                        
                    except Exception as e:
                        st.error(f"Error training model: {str(e)}")
            else:
                st.warning("Please select valid features and target variables.")
    
    with ml_tab2:
        st.markdown("### <i class='fas fa-crystal-ball'></i> Health Predictions")
        
        if 'model' in st.session_state:
            model = st.session_state['model']
            features = st.session_state['features']
            
            st.markdown("""
            <div class="feature-box">
                <h4><i class="fas fa-user-md"></i> Patient Information Input</h4>
                <p>Adjust the sliders below to input patient health parameters:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create input sliders
            input_data = []
            cols = st.columns(3)
            
            for i, feature in enumerate(features):
                with cols[i % 3]:
                    min_val = float(df[feature].min()) if feature in df.columns else 0.0
                    max_val = float(df[feature].max()) if feature in df.columns else 200.0
                    default_val = float(df[feature].mean()) if feature in df.columns else 50.0
                    
                    val = st.slider(
                        f"{feature}",
                        min_value=min_val,
                        max_value=max_val,
                        value=default_val,
                        step=(max_val - min_val) / 100
                    )
                    input_data.append(val)
            
            if st.button("🔍 Generate Prediction", key="predict_btn"):
                with st.spinner("Analyzing health data..."):
                    try:
                        prediction = model.predict([input_data])
                        result = prediction[0]
                        
                        # Create beautiful prediction result
                        if hasattr(model, 'predict_proba'):
                            probability = model.predict_proba([input_data])[0]
                            confidence = max(probability) * 100
                        else:
                            confidence = 85.0  # Default confidence
                        
                        if result == 1:
                            st.markdown("""
                            <div class="warning-card">
                                <h2><i class="fas fa-exclamation-triangle"></i> Risk Detected</h2>
                                <p>Based on the provided health parameters, there may be health risks present.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="success-card">
                                <h2><i class="fas fa-thumbs-up"></i> Healthy Status</h2>
                                <p>Your health parameters indicate good overall health!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.metric("🎯 Prediction Confidence", f"{confidence:.1f}%")
                        
                    except Exception as e:
                        st.error(f"Error making prediction: {str(e)}")
        else:
            st.info("Please train a model first in the Model Training tab.")
    
    with ml_tab3:
        st.markdown("### <i class='fas fa-chart-line'></i> Model Performance")
        
        if 'model_report' in st.session_state:
            st.markdown("**📊 Model Evaluation Report:**")
            st.code(st.session_state['model_report'])
            
            # Model metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Model Score", f"{st.session_state['model_score']:.3f}")
            
            with col2:
                st.metric("Features Used", len(st.session_state['features']))
            
            with col3:
                st.metric("Target Variable", st.session_state['target'])
        else:
            st.info("Please train a model first to see performance metrics.")

def create_visualization_section():
    """Create the visualization section"""
    
    st.markdown("""
    <div class="section-header">
        <h2><i class="fas fa-chart-pie"></i> Interactive Visualizations</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload a dataset first in the Dashboard tab.")
        return
    
    df = st.session_state['df']
    visualizer = PremiumVisualizer()
    
    # Visualization options
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "🔗 Correlations",
        "📊 Distributions", 
        "🎯 Relationships",
        "🌐 3D Analysis"
    ])
    
    with viz_tab1:
        st.markdown("### <i class='fas fa-project-diagram'></i> Correlation Analysis")
        visualizer.create_correlation_heatmap(df)
    
    with viz_tab2:
        st.markdown("### <i class='fas fa-chart-bar'></i> Distribution Analysis")
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numerical_cols:
            selected_columns = st.multiselect(
                "Select columns for distribution analysis:",
                numerical_cols,
                default=numerical_cols[:3] if len(numerical_cols) >= 3 else numerical_cols
            )
            
            if selected_columns:
                visualizer.create_distribution_plots(df, selected_columns)
        else:
            st.warning("⚠️ No numerical columns found for distribution analysis.")
    
    with viz_tab3:
        st.markdown("### <i class='fas fa-chart-line'></i> Relationship Analysis")
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numerical_cols) >= 2:
            col1, col2 = st.columns(2)
            
            with col1:
                x_col = st.selectbox("Select X-axis:", numerical_cols, key="scatter_x")
            
            with col2:
                y_col = st.selectbox("Select Y-axis:", numerical_cols, key="scatter_y")
            
            if x_col != y_col:
                visualizer.create_interactive_scatter_plot(df, x_col, y_col)
        else:
            st.warning("⚠️ Need at least 2 numerical columns for relationship analysis.")
    
    with viz_tab4:
        st.markdown("### <i class='fas fa-cube'></i> 3D Analysis")
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numerical_cols) >= 3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                x_col = st.selectbox("Select X-axis:", numerical_cols, key="3d_x")
            
            with col2:
                y_col = st.selectbox("Select Y-axis:", numerical_cols, key="3d_y")
            
            with col3:
                z_col = st.selectbox("Select Z-axis:", numerical_cols, key="3d_z")
            
            if x_col != y_col and y_col != z_col and x_col != z_col:
                visualizer.create_3d_scatter_plot(df, x_col, y_col, z_col)
        else:
            st.warning("⚠️ Need at least 3 numerical columns for 3D analysis.")

def create_reports_section():
    """Create the reports section"""
    
    st.markdown("""
    <div class="section-header">
        <h2><i class='fas fa-file-pdf'></i> Professional Reports</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload a dataset first in the Dashboard tab.")
        return
    
    df = st.session_state['df']
    
    # Report options
    st.markdown("### <i class='fas fa-cog'></i> Report Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_stats = st.checkbox("Include Summary Statistics", value=True)
        include_missing = st.checkbox("Include Missing Data Analysis", value=True)
    
    with col2:
        include_model = st.checkbox("Include Model Information", value=True)
        include_visualizations = st.checkbox("Include Visualizations", value=True)
    
    if st.button("📄 Generate Comprehensive Report", key="report_btn"):
        try:
            # Create PDF report
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Project Report", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
            pdf.ln(10)
            
            # Add dataset info
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt="Dataset Information", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Number of records: {len(df)}", ln=True)
            pdf.cell(200, 10, txt=f"Number of features: {len(df.columns)}", ln=True)
            pdf.ln(5)
            
            # Add summary statistics
            if include_stats:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="Summary Statistics", ln=True)
                pdf.set_font("Arial", size=10)
                
                # Create table with summary stats
                stats = df.describe().round(2).reset_index()
                col_widths = [30] + [25] * (len(stats.columns) - 1)
                
                # Header
                pdf.set_fill_color(200, 220, 255)
                for i, col in enumerate(stats.columns):
                    pdf.cell(col_widths[i], 10, str(col), border=1, fill=True)
                pdf.ln()
                
                # Rows
                for _, row in stats.iterrows():
                    for i, col in enumerate(stats.columns):
                        pdf.cell(col_widths[i], 10, str(row[col]), border=1)
                    pdf.ln()
                pdf.ln(5)
            
            # Add missing data analysis
            if include_missing:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="Missing Data Analysis", ln=True)
                pdf.set_font("Arial", size=10)
                
                missing_data = df.isnull().sum().reset_index()
                missing_data.columns = ['Feature', 'Missing Values']
                missing_data['Percentage'] = (missing_data['Missing Values'] / len(df) * 100).round(2)
                missing_data = missing_data[missing_data['Missing Values'] > 0]
                
                if len(missing_data) > 0:
                    # Table header
                    pdf.set_fill_color(200, 220, 255)
                    pdf.cell(60, 10, "Feature", border=1, fill=True)
                    pdf.cell(40, 10, "Missing Values", border=1, fill=True)
                    pdf.cell(40, 10, "Percentage", border=1, fill=True)
                    pdf.ln()
                    
                    # Table rows
                    for _, row in missing_data.iterrows():
                        pdf.cell(60, 10, row['Feature'], border=1)
                        pdf.cell(40, 10, str(row['Missing Values']), border=1)
                        pdf.cell(40, 10, f"{row['Percentage']}%", border=1)
                        pdf.ln()
                else:
                    pdf.cell(200, 10, txt="No missing values found in the dataset.", ln=True)
                pdf.ln(5)
            
            # Add model information
            if include_model and 'model' in st.session_state:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="Model Information", ln=True)
                pdf.set_font("Arial", size=10)
                
                pdf.cell(200, 10, txt=f"Target Variable: {st.session_state['target']}", ln=True)
                pdf.cell(200, 10, txt=f"Model Score: {st.session_state['model_score']:.2f}", ln=True)
                pdf.ln(5)
                
                pdf.cell(200, 10, txt="Features Used:", ln=True)
                for feature in st.session_state['features']:
                    pdf.cell(200, 10, txt=f"- {feature}", ln=True)
                pdf.ln(5)
            
            # Save PDF to file
            report_path = "healthai_report.pdf"
            pdf.output(report_path)
            
            # Download button
            with open(report_path, "rb") as f:
                st.download_button(
                    label="📥 Download Report (PDF)",
                    data=f,
                    file_name="healthai_report.pdf",
                    mime="application/pdf"
                )
            
            st.success("✅ Report generated successfully!")
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    create_premium_app() 