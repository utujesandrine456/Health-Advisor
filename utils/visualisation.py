import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List
import streamlit as st

class Visualizer:
    """Class for creating interactive visualizations"""
    
    def __init__(self, df):
        """Initialize with standardized column names"""
        self.df = df.copy()
        self.df.columns = self.df.columns.str.lower()  # Standardize to lowercase
        self.available_features = [col for col in self.df.columns 
                                 if col != 'outcome' and 
                                 pd.api.types.is_numeric_dtype(self.df[col])]
        
    def _validate_column(self, column_name):
        """Check if column exists (case insensitive)"""
        return next((col for col in self.df.columns 
                   if col.lower() == column_name.lower()), None)
    
    def plot_histogram(self, column_name, title):
        """Plot histogram with robust column name handling"""
        # Find the actual column names (case insensitive)
        x_col = next((col for col in self.df.columns if col.lower() == column_name.lower()), None)
        color_col = next((col for col in self.df.columns if col.lower() == 'outcome'), None)
        
        if not x_col:
            raise ValueError(f"Column '{column_name}' not found. Available columns: {list(self.df.columns)}")
        
        fig = px.histogram(
            self.df,
            x=x_col,
            color=color_col,  # Will be None if outcome column doesn't exist
            title=title,
            nbins=30,
            color_discrete_map={0: "blue", 1: "red"} if color_col else None
        )
        return fig
    
    def plot_boxplot(self, column: str, title: str) -> go.Figure:
        """Create a boxplot for a given column
        
        Args:
            column: Name of the column to plot
            title: Title of the plot
            
        Returns:
            plotly.graph_objects.Figure: Interactive boxplot
        """
        fig = px.box(
            self.df,
            y=column,
            color='Outcome',
            title=title,
            color_discrete_sequence=['#764ba2', '#667eea']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            yaxis_title=column,
            xaxis_title='Outcome',
            legend_title='Diabetes Outcome'
        )
        return fig
    
    def plot_scatter(self, x_col: str, y_col: str, title: str) -> go.Figure:
        """Create a scatter plot between two columns
        
        Args:
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column
            title: Title of the plot
            
        Returns:
            plotly.graph_objects.Figure: Interactive scatter plot
        """
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color='Outcome',
            title=title,
            color_discrete_sequence=['#764ba2', '#667eea'],
            trendline='lowess'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            xaxis_title=x_col,
            yaxis_title=y_col,
            legend_title='Diabetes Outcome',
            hovermode='closest'
        )
        return fig
    
    def plot_correlation_heatmap(self) -> go.Figure:
        """Create a correlation matrix heatmap
        
        Returns:
            plotly.graph_objects.Figure: Interactive correlation heatmap
        """
        # Select only numeric columns
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        corr = numeric_df.corr()
        
        # Create heatmap using graph_objects for more control
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            text=corr.values.round(2),
            texttemplate='%{text}',
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            colorbar=dict(
                title=dict(
                    text='Correlation',
                    font=dict(size=14)
                ),
                tickfont=dict(size=12)
            )
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='Feature Correlation Heatmap',
                x=0.5,
                font=dict(size=24)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family='Arial',
                color='#2c3e50'
            ),
            width=800,
            height=800,
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                tickfont=dict(size=12)
            )
        )
        
        return fig
    
    def plot_pie_chart(self, column: str, title: str) -> go.Figure:
        """Create a pie chart for categorical data
        
        Args:
            column: Name of the column to plot
            title: Title of the plot
            
        Returns:
            plotly.graph_objects.Figure: Interactive pie chart
        """
        fig = px.pie(
            self.df,
            names=column,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            legend_title=column,
            uniformtext_minsize=12,
            uniformtext_mode='hide'
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            pull=[0.1, 0] if len(self.df[column].unique()) == 2 else None
        )
        return fig
    
    def plot_violin(self, column: str, title: str) -> go.Figure:
        """Create a violin plot for a given column
        
        Args:
            column: Name of the column to plot
            title: Title of the plot
            
        Returns:
            plotly.graph_objects.Figure: Interactive violin plot
        """
        fig = px.violin(
            self.df,
            y=column,
            color='Outcome',
            title=title,
            color_discrete_sequence=['#764ba2', '#667eea'],
            box=True,
            points='all'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            yaxis_title=column,
            xaxis_title='Outcome',
            legend_title='Diabetes Outcome'
        )
        return fig
    
    def plot_3d_scatter(self, x_col: str, y_col: str, z_col: str, title: str) -> go.Figure:
        """Create a 3D scatter plot
        
        Args:
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column
            z_col: Name of the z-axis column
            title: Title of the plot
            
        Returns:
            plotly.graph_objects.Figure: Interactive 3D scatter plot
        """
        fig = px.scatter_3d(
            self.df,
            x=x_col,
            y=y_col,
            z=z_col,
            color='Outcome',
            title=title,
            color_discrete_sequence=['#764ba2', '#667eea'],
            opacity=0.7
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            ),
            legend_title='Diabetes Outcome',
            margin=dict(l=0, r=0, b=0, t=30)
        )
        return fig
        
    def plot_pairplot(self, features: List[str], title: str = "Feature Relationships") -> go.Figure:
        """Create a pairplot matrix for selected features
        
        Args:
            features: List of column names to include in the pairplot
            title: Title of the plot
            
        Returns:
            plotly.graph_objects.Figure: Interactive pairplot matrix
        """
        # Create a subplot grid based on number of features
        n_features = len(features)
        fig = make_subplots(
            rows=n_features, 
            cols=n_features,
            subplot_titles=[f"{x} vs {y}" for x in features for y in features]
        )
        
        # Add scatter plots for each feature combination
        for i, feat1 in enumerate(features, 1):
            for j, feat2 in enumerate(features, 1):
                if feat1 != feat2:
                    # Scatter plot
                    fig.add_trace(
                        go.Scatter(
                            x=self.df[feat1],
                            y=self.df[feat2],
                            mode='markers',
                            marker=dict(
                                color=self.df['Outcome'],
                                colorscale=['#764ba2', '#667eea'],
                                showscale=False
                            ),
                            showlegend=False
                        ),
                        row=i, col=j
                    )
                else:
                    # Histogram for diagonal
                    fig.add_trace(
                        go.Histogram(
                            x=self.df[feat1],
                            nbinsx=30,
                            marker_color='#764ba2',
                            showlegend=False
                        ),
                        row=i, col=j
                    )
        
        # Update layout
        fig.update_layout(
            title=title,
            height=200 * n_features,
            width=200 * n_features,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    

    def plot_outcome_comparison(self, feature):
        """Compare feature distribution by diabetes outcome"""
        try:
            # Find outcome column (case insensitive)
            outcome_col = next((col for col in self.df.columns 
                            if col.lower() == 'outcome'), None)
            
            if outcome_col is None:
                st.warning("No outcome column found for comparison")
                return None
                
            if feature not in self.df.columns:
                st.warning(f"Feature '{feature}' not found in data")
                return None
                
            fig = px.box(
                self.df,
                x=outcome_col,
                y=feature,
                color=outcome_col,
                title=f"{feature} by Diabetes Outcome",
                labels={outcome_col: "Diabetes Diagnosis", feature: feature},
                color_discrete_map={0: "blue", 1: "red"}
            )
            
            fig.update_layout(
                xaxis_title="Diabetes Diagnosis (0=No, 1=Yes)",
                yaxis_title=feature
            )
            return fig
            
        except Exception as e:
            st.error(f"Error creating comparison plot: {str(e)}")
            return None

    def plot_pairplot(self, features):
        """Create a pair plot for selected features"""
        try:
            if len(features) < 2:
                st.warning("Please select at least 2 features")
                return None
                
            # Handle outcome column if it exists
            color_col = next((col for col in self.df.columns 
                            if col.lower() == 'outcome'), None)
            
            fig = px.scatter_matrix(
                self.df,
                dimensions=features,
                color=color_col,
                title="Feature Relationships",
                color_discrete_map={0: "blue", 1: "red"} if color_col else None
            )
            fig.update_traces(diagonal_visible=False)
            return fig
            
        except Exception as e:
            st.error(f"Failed to create pair plot: {str(e)}")
            return None
        

    
    def plot_correlation_heatmap(self):
        """Plot correlation heatmap for numeric features"""
        try:
            numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
            if len(numeric_df.columns) < 2:
                st.warning("Not enough numeric features for correlation")
                return None
                
            corr_matrix = numeric_df.corr()
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu',
                range_color=[-1, 1],
                title="Feature Correlation Heatmap"
            )
            return fig
        except Exception as e:
            st.error(f"Correlation heatmap error: {str(e)}")
            return None


    

    def plot_line(self, x_col: str, y_col: str, title: str, group_by: Optional[str] = None) -> go.Figure:
        """Create a line plot between two columns with optional grouping
        
        Args:
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column  
            title: Title of the plot
            group_by: Column to group/color lines by (default: None)
            
        Returns:
            plotly.graph_objects.Figure: Interactive line plot
        """
        fig = px.line(
            self.df,
            x=x_col,
            y=y_col,
            color=group_by,
            title=title,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode='x unified'
        )
        
        if group_by:
            fig.update_layout(legend_title=group_by)
        
        return fig




    def plot_scatter(self, x_col: str, y_col: str, title: str, size_col: Optional[str] = None, hover_data: Optional[List[str]] = None) -> go.Figure:
        """Enhanced scatter plot with size and hover data options
        
        Args:
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column
            title: Title of the plot
            size_col: Column to use for marker sizes (optional)
            hover_data: Additional columns to show in hover (optional)
            
        Returns:
            plotly.graph_objects.Figure: Interactive scatter plot
        """
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color='outcome',
            size=size_col,
            hover_data=hover_data,
            title=title,
            color_discrete_sequence=['#764ba2', '#667eea'],
            trendline='lowess'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            xaxis_title=x_col,
            yaxis_title=y_col,
            legend_title='Diabetes Outcome',
            hovermode='closest'
        )
        
        if size_col:
            fig.update_layout(legend_title_text=f'Outcome (Size: {size_col})')
        
        return fig

    


    def plot_bar(self, x_col: str, y_col: str, title: str, barmode: str = 'group', orientation: str = 'v') -> go.Figure:
        """Create a bar graph comparing values
        
        Args:
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column  
            title: Title of the plot
            barmode: 'group', 'stack', or 'relative' 
            orientation: 'v' (vertical) or 'h' (horizontal)
            
        Returns:
            plotly.graph_objects.Figure: Interactive bar graph
        """
        fig = px.bar(
            self.df,
            x=x_col,
            y=y_col,
            color='outcome',
            title=title,
            barmode=barmode,
            orientation=orientation,
            color_discrete_sequence=['#764ba2', '#667eea']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            xaxis_title=x_col if orientation == 'v' else y_col,
            yaxis_title=y_col if orientation == 'v' else x_col,
            legend_title='Diabetes Outcome',
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
        
        return fig


        
class PremiumVisualizer:
    """Premium visualization class with advanced features for the health advisor app"""
    
    def __init__(self):
        """Initialize the premium visualizer"""
        pass
    
    def create_correlation_heatmap(self, df):
        """Create an interactive correlation heatmap"""
        numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numerical_cols) < 2:
            st.warning("⚠️ Need at least 2 numerical columns for correlation analysis.")
            return
        
        # Calculate correlation matrix
        corr_matrix = df[numerical_cols].corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap",
            color_continuous_scale="RdBu_r"
        )
        
        fig.update_layout(
            width=800,
            height=600,
            title_x=0.5,
            font=dict(size=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show correlation insights
        st.markdown("### 📊 Correlation Insights")
        
        # Find strongest correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))
        
        # Sort by absolute correlation
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔗 Strongest Positive Correlations:**")
            for i, (col1, col2, corr) in enumerate(corr_pairs[:5]):
                if corr > 0.5:
                    st.success(f"• {col1} ↔ {col2}: {corr:.3f}")
        
        with col2:
            st.markdown("**🔗 Strongest Negative Correlations:**")
            for i, (col1, col2, corr) in enumerate(corr_pairs[:5]):
                if corr < -0.5:
                    st.error(f"• {col1} ↔ {col2}: {corr:.3f}")
    
    def create_distribution_plots(self, df, columns):
        """Create distribution plots for selected columns"""
        if len(columns) == 0:
            st.warning("⚠️ Please select at least one column for distribution analysis.")
            return
        
        # Create subplots
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig = make_subplots(
            rows=n_rows, cols=n_cols,
            subplot_titles=columns,
            specs=[[{"secondary_y": False}] * n_cols] * n_rows
        )
        
        for i, col in enumerate(columns):
            row = i // n_cols + 1
            col_idx = i % n_cols + 1
            
            # Create histogram
            fig.add_trace(
                go.Histogram(
                    x=df[col].dropna(),
                    name=col,
                    nbinsx=30,
                    marker_color='#667eea'
                ),
                row=row, col=col_idx
            )
        
        fig.update_layout(
            height=300 * n_rows,
            title_text="Distribution Analysis",
            showlegend=False,
            title_x=0.5
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show statistics
        st.markdown("### 📊 Distribution Statistics")
        
        stats_df = df[columns].describe().round(3)
        st.dataframe(stats_df, use_container_width=True)
    
    def create_interactive_scatter_plot(self, df, x_col, y_col):
        """Create an interactive scatter plot"""
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=f"Relationship: {x_col} vs {y_col}",
            trendline="ols",
            color_discrete_sequence=['#667eea']
        )
        
        fig.update_layout(
            width=800,
            height=600,
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate correlation
        correlation = df[x_col].corr(df[y_col])
        st.metric("Correlation Coefficient", f"{correlation:.3f}")
    
    def create_3d_scatter_plot(self, df, x_col, y_col, z_col):
        """Create a 3D scatter plot"""
        fig = px.scatter_3d(
            df,
            x=x_col,
            y=y_col,
            z=z_col,
            title=f"3D Analysis: {x_col} vs {y_col} vs {z_col}",
            color_discrete_sequence=['#667eea']
        )
        
        fig.update_layout(
            width=800,
            height=600,
            title_x=0.5,
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        

        