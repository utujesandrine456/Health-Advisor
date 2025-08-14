# 🏥 Health Tracker - Premium Health Analytics Platform

A modern, interactive health analytics and machine learning platform built with Streamlit. This application provides comprehensive data analysis, visualization, and predictive modeling capabilities for health datasets.

## ✨ Features

### 🎯 Core Features
- **📊 Advanced Data Analytics**: Comprehensive statistical analysis and insights
- **🤖 Machine Learning**: Predictive modeling with multiple algorithms
- **📈 Interactive Visualizations**: Beautiful, responsive charts and graphs
- **📄 Professional Reports**: Generate PDF reports with detailed analysis
- **🔍 Data Quality Analysis**: Automatic data cleaning and validation
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

### 🎨 Premium UI/UX
- **Modern Design**: Gradient backgrounds and smooth animations
- **Interactive Elements**: Hover effects and dynamic content
- **Professional Styling**: Clean, medical-grade interface
- **Accessibility**: High contrast and readable fonts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Health-Tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app/main_app.py
   ```
   
   Or use the launcher script:
   ```bash
   python run_app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
Health Tracker/
├── app/
│   ├── main_app.py          # Main application file
│   └── __init__.py
├── utils/
│   ├── data_cleaning.py     # Data cleaning utilities
│   ├── visualisation.py     # Visualization tools
│   ├── model.py            # Machine learning models
│   ├── insights.py         # Data insights generation
│   ├── data_loader.py      # Data loading utilities
│   └── __init__.py
├── assets/
│   ├── style.css           # Premium CSS styling
│   └── images/             # Application images
├── data/
│   ├── diabetes.csv        # Sample diabetes dataset
│   ├── diabetes_messy.csv  # Messy version for testing
│   └── heart.csv           # Sample heart disease dataset
├── models/                 # Trained model storage
├── notebooks/
│   └── EDA.ipynb          # Exploratory data analysis
├── requirements.txt        # Python dependencies
├── run_app.py             # Application launcher
└── README.md              # This file
```

## 🎯 Application Modules

### 1. 🏠 Dashboard
- **Data Upload**: Drag-and-drop CSV file upload
- **Data Overview**: Quick statistics and data quality metrics
- **Real-time Processing**: Automatic data cleaning and validation

### 2. 📊 Analytics
- **Descriptive Statistics**: Comprehensive statistical summaries
- **Data Quality Analysis**: Missing values, outliers, and data types
- **Trend Analysis**: Time-series analysis for temporal data

### 3. 🤖 Machine Learning
- **Model Training**: Train custom machine learning models
- **Predictions**: Interactive prediction interface with sliders
- **Model Performance**: Detailed evaluation metrics and reports

### 4. 📈 Visualizations
- **Correlation Analysis**: Interactive correlation heatmaps
- **Distribution Plots**: Histograms and box plots
- **Relationship Analysis**: Scatter plots with trend lines
- **3D Analysis**: Three-dimensional scatter plots

### 5. 📄 Reports
- **PDF Generation**: Professional reports with charts and tables
- **Customizable Content**: Select sections to include
- **Download Options**: Easy export functionality

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms
- **Plotly**: Interactive visualizations
- **Matplotlib/Seaborn**: Statistical plotting
- **FPDF**: PDF report generation

### Key Classes

#### `AdvancedDataCleaner`
- Comprehensive data cleaning pipeline
- Missing value handling
- Outlier detection and treatment
- Column standardization

#### `PremiumVisualizer`
- Interactive correlation heatmaps
- Distribution analysis
- Relationship visualization
- 3D plotting capabilities

#### `DiabetesPredictor`
- Random Forest classification
- Model persistence
- Performance evaluation
- Feature importance analysis

## 📊 Supported Data Formats

- **CSV Files**: Primary format with automatic detection
- **Excel Files**: .xlsx and .xls support
- **Text Files**: Tab-separated and comma-separated values

## 🎨 Customization

### Styling
The application uses a custom CSS file (`assets/style.css`) with:
- Modern gradient backgrounds
- Smooth animations and transitions
- Responsive design elements
- Professional color schemes

### Adding New Features
1. Create new functions in the appropriate utility module
2. Import and integrate into `main_app.py`
3. Update the UI components as needed
4. Test with sample datasets

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **CSS Not Loading**
   - Ensure `assets/style.css` exists
   - Check file permissions

3. **Model Training Errors**
   - Verify dataset has sufficient numerical columns
   - Check for missing values in target variable

4. **Memory Issues**
   - Reduce dataset size for testing
   - Close other applications

### Performance Tips
- Use smaller datasets for development
- Enable caching for expensive operations
- Optimize visualizations for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- Scikit-learn for machine learning tools
- The open-source community for inspiration

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the documentation
3. Open an issue on GitHub
4. Contact the development team

---

**Made with ❤️ for better health analytics**




