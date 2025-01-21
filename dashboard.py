import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Panel de Ventas", layout="wide")

# Title
st.title("📊 Panel de Análisis de Ventas")

# Load the data
@st.cache_data
def load_data():
    try:
        # Define file paths relative to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'data')
        
        # Get all CSV files in the data directory
        files = {}
        for file in os.listdir(data_dir):
            if file.startswith('sales_analysis_') and file.endswith('.csv'):
                # Extract location name from filename
                location = file.replace('sales_analysis_', '').split('_')[0]
                files[location] = os.path.join(data_dir, file)
        
        # Read and combine all files
        dfs = []
        for location, file_path in files.items():
            if not os.path.exists(file_path):
                st.error(f"Archivo no encontrado: {file_path}")
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
        st.error(f"Error al cargar los datos: {e}")
        return None

df = load_data()

if df is not None:
    # Sidebar for global filters
    st.sidebar.title("Filtros Globales")
    selected_locations = st.sidebar.multiselect(
        "Seleccionar Locales",
        options=df['Location'].unique(),
        default=df['Location'].unique()
    )
    
    # Filter data based on selected locations
    df_filtered = df[df['Location'].isin(selected_locations)]
    
    # Display basic info with metrics
    st.subheader("📈 Métricas Principales")
    col1, col2, col3 = st.columns(3)
    
    numeric_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 0:
        with col1:
            total_sales = df_filtered[numeric_cols[0]].sum()
            st.metric("Ventas Totales", f"${total_sales:,.2f}")
        with col2:
            store_averages = df_filtered.groupby('Location')[numeric_cols[0]].sum().mean()
            st.metric("Promedio de Ventas por Local", f"${store_averages:,.2f}")
        with col3:
            locations_count = len(selected_locations)
            st.metric("Locales Analizados", locations_count)
    
    # Create tabs for different analyses
    tab1, tab2 = st.tabs(["📊 Análisis de Ventas", "🔍 Comparación Detallada"])
    
    with tab1:
        st.subheader("Distribución de Ventas por Local")
        
        # Sales distribution
        if len(numeric_cols) > 0:
            # Bar chart for sales performance
            agg_data = df_filtered.groupby('Location')[numeric_cols[0]].agg(['sum', 'mean']).reset_index()
            fig_bar = go.Figure(data=[
                go.Bar(name='Ventas Totales', x=agg_data['Location'], y=agg_data['sum'], marker_color='lightblue'),
                go.Bar(name='Venta Promedio', x=agg_data['Location'], y=agg_data['mean'], marker_color='darkblue')
            ])
            fig_bar.update_layout(
                title="Rendimiento de Ventas por Local",
                barmode='group',
                xaxis_title="Local",
                yaxis_title="Monto ($)",
                template="plotly_dark"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("Comparación de Rendimiento por Local")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if len(numeric_cols) > 0:
                # Create ranking by total sales
                sales_ranking = df_filtered.groupby('Location')[numeric_cols[0]].sum().sort_values(ascending=False)
                
                # Calculate average sales per store
                avg_store_sales = sales_ranking.mean()
                
                # Create DataFrame with performance categories
                ranking_df = pd.DataFrame({
                    'Posición': range(1, len(sales_ranking) + 1),
                    'Local': sales_ranking.index,
                    'Ventas Totales': sales_ranking.values,
                    'Rendimiento': ['Sobre Promedio' if x > avg_store_sales else 'Bajo Promedio' for x in sales_ranking.values]
                })
                
                # Display ranking
                st.write("🏆 Ranking de Locales por Ventas Totales")
                st.dataframe(
                    ranking_df.style.format({
                        'Ventas Totales': '${:,.2f}'
                    }).bar(subset=['Ventas Totales'], color='lightblue'),
                    use_container_width=True
                )
                
                # Create performance comparison chart
                st.write("📈 Rendimiento vs Promedio")
                
                # Calculate percentage difference from average
                ranking_df['Diferencia del Promedio'] = ((ranking_df['Ventas Totales'] - avg_store_sales) / avg_store_sales) * 100
                
                # Create bar chart
                fig_performance = go.Figure()
                
                # Add bars
                colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in ranking_df['Diferencia del Promedio']]
                
                fig_performance.add_trace(go.Bar(
                    x=ranking_df['Local'],
                    y=ranking_df['Diferencia del Promedio'],
                    marker_color=colors,
                    text=[f"{x:,.1f}%" for x in ranking_df['Diferencia del Promedio']],
                    textposition='auto',
                ))
                
                # Add horizontal line at 0
                fig_performance.add_hline(y=0, line_dash="dash", line_color="white")
                
                # Update layout
                fig_performance.update_layout(
                    title="Diferencia Porcentual del Promedio de Ventas",
                    xaxis_title="Local",
                    yaxis_title="% Diferencia del Promedio",
                    template="plotly_dark",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_performance, use_container_width=True)
        
        with col2:
            # Pie chart of total sales by location
            sales_by_location = df_filtered.groupby('Location')[numeric_cols[0]].sum()
            fig_pie = px.pie(values=sales_by_location.values,
                           names=sales_by_location.index,
                           title="Distribución de Ventas por Local")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Add performance summary
            above_avg = len(ranking_df[ranking_df['Rendimiento'] == 'Sobre Promedio'])
            below_avg = len(ranking_df[ranking_df['Rendimiento'] == 'Bajo Promedio'])
            
            st.write("📊 Resumen de Rendimiento")
            summary_col1, summary_col2 = st.columns(2)
            with summary_col1:
                st.metric("Sobre Promedio", f"{above_avg} locales")
            with summary_col2:
                st.metric("Bajo Promedio", f"{below_avg} locales")
    
    # Get categorical columns for filtering
    categorical_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()
    categorical_cols.remove('Location')
    
    # Advanced Filtering Section
    st.subheader("🔍 Explorador de Datos Avanzado")
    col1, col2 = st.columns(2)
    
    with col1:
        if len(categorical_cols) > 0:
            filter_col = st.selectbox("Filtrar por:", categorical_cols)
            selected_values = st.multiselect(
                "Seleccionar valores:",
                options=df_filtered[filter_col].unique()
            )
    
    # Apply filters
    if len(categorical_cols) > 0 and selected_values:
        df_filtered = df_filtered[df_filtered[filter_col].isin(selected_values)]
    
    # Show filtered data with improved formatting
    if len(df_filtered) > 0:
        st.write("📋 Datos Filtrados:")
        st.dataframe(
            df_filtered.style.format({
                col: "${:,.2f}" for col in numeric_cols
            }),
            use_container_width=True
        )

else:
    st.error("❌ Error al cargar los archivos de datos. Por favor, verifique que todos los archivos existan y sean accesibles.") 