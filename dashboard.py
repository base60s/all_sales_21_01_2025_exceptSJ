import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Sales Analysis Dashboard", layout="wide")

# Title
st.title("📊 Sales Analysis Dashboard")

# Load the data
@st.cache_data
def load_data():
    try:
        # Define file paths
        base_dir = os.path.expanduser("~/Downloads")
        
        # Dictionary of all store files
        files = {
            'Azcuénaga': os.path.join(base_dir, 'extracted_report_Azcuénaga/sales_analysis_Azcuénaga_20250121_181153.csv'),
            'Colon_Brunch': os.path.join(base_dir, 'extracted_report_Colon_Brunch/sales_analysis_Colon_Brunch_20250121_180411.csv'),
            'Viamonte': os.path.join(base_dir, 'extracted_report_Viamonte/sales_analysis_Viamonte_20250121_181318.csv'),
            'Chacras': os.path.join(base_dir, 'extracted_report_Chacras/sales_analysis_Chacras_20250121_184204.csv'),
            'ElPidio': os.path.join(base_dir, 'extracted_report_ElPidio/sales_analysis_ElPidio_20250121_183024.csv'),
            'Pizzabox': os.path.join(base_dir, 'extracted_report_Pizzabox/sales_analysis_Pizzabox_20250121_182151.csv'),
            'Palero': os.path.join(base_dir, 'extracted_report_Palero/sales_analysis_Palero_20250121_180246.csv'),
            'Tiburcio': os.path.join(base_dir, 'extracted_report_Tiburcio/sales_analysis_Tiburcio_20250121_182858.csv'),
            'PuenteOlive': os.path.join(base_dir, 'extracted_report_PuenteOlive/sales_analysis_PuenteOlive_20250121_182733.csv'),
            'Panamericana': os.path.join(base_dir, 'extracted_report_Panamericana/sales_analysis_Panamericana_20250121_182025.csv'),
            'Centro': os.path.join(base_dir, 'extracted_report_Centro/sales_analysis_Centro_20250121_184330.csv'),
            'Cervantes': os.path.join(base_dir, 'extracted_report_Cervantes/sales_analysis_Cervantes_20250121_180537.csv'),
            'Colon1': os.path.join(base_dir, 'extracted_report_Colon1/sales_analysis_Colon1_20250121_180902.csv'),
            'GodoyCruz': os.path.join(base_dir, 'extracted_report_GodoyCruz/sales_analysis_GodoyCruz_20250121_181028.csv'),
            'Dorrego': os.path.join(base_dir, 'extracted_report_Dorrego/sales_analysis_Dorrego_20250121_182442.csv'),
            'Vistalba': os.path.join(base_dir, 'extracted_report_Vistalba/sales_analysis_Vistalba_20250121_181444.csv'),
            'JBJ': os.path.join(base_dir, 'extracted_report_JBJ/sales_analysis_JBJ_20250121_181900.csv'),
            'Beltran': os.path.join(base_dir, 'extracted_report_Beltran/sales_analysis_Beltran_20250121_181609.csv'),
            'Jac': os.path.join(base_dir, 'extracted_report_Jac/sales_analysis_Jac_20250121_181734.csv'),
            'Rotonda': os.path.join(base_dir, 'extracted_report_Rotonda/sales_analysis_Rotonda_20250121_180120.csv'),
            'SJ_Shell': os.path.join(base_dir, 'extracted_report_SJ_Shell/sales_analysis_SJ_Shell_20250121_183224.csv'),
            'Avellaneda': os.path.join(base_dir, 'extracted_report_Avellaneda/sales_analysis_Avellaneda_20250121_182607.csv'),
            'Sarmiento': os.path.join(base_dir, 'extracted_report_Sarmiento/sales_analysis_Sarmiento_20250121_182316.csv'),
            'Tunuyan_LV': os.path.join(base_dir, 'extracted_report_Tunuyan_LV/sales_analysis_Tunuyan_LV_20250121_190651.csv')
        }
        
        # Read and combine all files
        dfs = []
        for location, file_path in files.items():
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                continue
            df = pd.read_csv(file_path)
            df['Location'] = location
            dfs.append(df)
        
        if not dfs:
            return None
            
        # Combine all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Remove 'Cantidad' from analysis
        if 'Cantidad' in combined_df.columns:
            combined_df = combined_df.drop('Cantidad', axis=1)
            
        return combined_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # Sidebar for global filters
    st.sidebar.title("Global Filters")
    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        options=df['Location'].unique(),
        default=df['Location'].unique()
    )
    
    # Filter data based on selected locations
    df_filtered = df[df['Location'].isin(selected_locations)]
    
    # Display basic info with metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    numeric_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 0:
        with col1:
            total_sales = df_filtered[numeric_cols[0]].sum()
            st.metric("Total Sales", f"${total_sales:,.2f}")
        with col2:
            avg_sales = df_filtered[numeric_cols[0]].mean()
            st.metric("Average Sales", f"${avg_sales:,.2f}")
        with col3:
            locations_count = len(selected_locations)
            st.metric("Locations Analyzed", locations_count)
    
    # Create tabs for different analyses
    tab1, tab2 = st.tabs(["📊 Sales Analysis", "🔍 Detailed Comparison"])
    
    with tab1:
        st.subheader("Sales Distribution by Location")
        
        # Sales distribution
        if len(numeric_cols) > 0:
            # Bar chart for sales performance
            agg_data = df_filtered.groupby('Location')[numeric_cols[0]].agg(['sum', 'mean']).reset_index()
            fig_bar = go.Figure(data=[
                go.Bar(name='Total Sales', x=agg_data['Location'], y=agg_data['sum'], marker_color='lightblue'),
                go.Bar(name='Average Sale', x=agg_data['Location'], y=agg_data['mean'], marker_color='darkblue')
            ])
            fig_bar.update_layout(
                title="Sales Performance by Location",
                barmode='group',
                xaxis_title="Location",
                yaxis_title="Amount ($)",
                template="plotly_dark"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("Location Performance Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if len(numeric_cols) > 0:
                # Summary statistics
                summary_stats = df_filtered.groupby('Location')[numeric_cols[0]].agg([
                    'mean', 'median', 'std', 'min', 'max', 'count'
                ]).round(2)
                
                # Format the summary statistics
                summary_stats.columns = ['Average', 'Median', 'Std Dev', 'Min', 'Max', 'Count']
                st.write("📊 Summary Statistics by Location")
                st.dataframe(summary_stats, use_container_width=True)
        
        with col2:
            # Pie chart of total sales by location
            sales_by_location = df_filtered.groupby('Location')[numeric_cols[0]].sum()
            fig_pie = px.pie(values=sales_by_location.values,
                           names=sales_by_location.index,
                           title="Sales Distribution by Location")
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Get categorical columns for filtering
    categorical_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()
    categorical_cols.remove('Location')
    
    # Advanced Filtering Section
    st.subheader("🔍 Advanced Data Explorer")
    col1, col2 = st.columns(2)
    
    with col1:
        if len(categorical_cols) > 0:
            filter_col = st.selectbox("Filter by:", categorical_cols)
            selected_values = st.multiselect(
                "Select values:",
                options=df_filtered[filter_col].unique()
            )
    
    # Apply filters
    if len(categorical_cols) > 0 and selected_values:
        df_filtered = df_filtered[df_filtered[filter_col].isin(selected_values)]
    
    # Show filtered data with improved formatting
    if len(df_filtered) > 0:
        st.write("📋 Filtered Data:")
        st.dataframe(
            df_filtered.style.format({
                col: "${:,.2f}" for col in numeric_cols
            }),
            use_container_width=True
        )

else:
    st.error("❌ Failed to load the data files. Please check if all files exist and are accessible.") 