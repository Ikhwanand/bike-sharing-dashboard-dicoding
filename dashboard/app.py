# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from sklearn.preprocessing import MinMaxScaler

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    daily_df = pd.read_csv('./data/day.csv')
    daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
    return daily_df

# Load the data
daily_df = load_data()

# Sidebar
st.sidebar.title("Bike Sharing Analysis")
st.sidebar.image("https://img.freepik.com/free-vector/modern-cycling-adventure-icon-isolated_24877-83359.jpg?t=st=1740796331~exp=1740799931~hmac=8df5655ae183cd3d3ce4325a4fcff4508cbfc57dcee4a5f900b0d0dd8602830d&w=740", use_container_width=True)

with st.sidebar:
    st.sidebar.markdown("### Select Parameters")
    date_range = st.sidebar.date_input(
        "Select a date range",
        value=(daily_df['dteday'].min(), daily_df['dteday'].max()),
        min_value=daily_df['dteday'].min(),
        max_value=daily_df['dteday'].max(),
        key='date_range'
    )
    start_date, end_date = pd.to_datetime(date_range)
    daily_df = daily_df[(daily_df['dteday'] >= start_date) & (daily_df['dteday'] <= end_date)]



# Main page title
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analysis of bike sharing patterns and user behavior")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Overview", "RFM Analysis", "Segmentation"])

# Tab 1: Overview
with tab1:
    # Row 1
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_rentals = daily_df['cnt'].sum()
        st.metric("Total Rentals", f"{total_rentals:,}")
    
    with col2:
        avg_daily_rentals = daily_df['cnt'].mean()
        st.metric("Average Daily Rentals", f"{avg_daily_rentals:.0f}")
    
    with col3:
        total_days = len(daily_df)
        st.metric("Total Days", total_days)

    # Row 2
    st.subheader("Rental Trends")
    
    # Time series plot
    fig_trend = px.line(daily_df, 
                       x='dteday', 
                       y=['casual', 'registered', 'cnt'],
                       title='Rental Trends Over Time')
    st.plotly_chart(fig_trend, use_container_width=True)

    # Row 3
    col1, col2 = st.columns(2)

    with col1:
        # Seasonal pattern
        seasonal_avg = daily_df.groupby('season')['cnt'].mean().reset_index()
        fig_seasonal = px.bar(seasonal_avg, 
                            x='season', 
                            y='cnt',
                            title='Average Rentals by Season')
        st.plotly_chart(fig_seasonal, use_container_width=True)

    with col2:
        # Weather impact
        weather_avg = daily_df.groupby('weathersit')['cnt'].mean().reset_index()
        fig_weather = px.bar(weather_avg, 
                           x='weathersit', 
                           y='cnt',
                           title='Average Rentals by Weather')
        st.plotly_chart(fig_weather, use_container_width=True)

# Tab 2: RFM Analysis
with tab2:
    st.subheader("RFM (Recency, Frequency, Monetary) Analysis")

    # Calculate RFM metrics
    last_date = daily_df['dteday'].max() + pd.Timedelta(days=1)
    
    rfm_data = daily_df.groupby(['season']).agg({
        'dteday': lambda x: (last_date - x.max()).days,  # Recency
        'cnt': ['count', 'mean']  # Frequency and Monetary
    }).round(2)

    # Flatten column names
    rfm_data.columns = ['Recency', 'Frequency', 'Average_Rentals']
    rfm_data = rfm_data.reset_index()

    # Create season labels
    season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    rfm_data['Season'] = rfm_data['season'].map(season_labels)

    # RFM Visualization
    col1, col2 = st.columns(2)

    with col1:
        fig_rfm = px.bar(rfm_data, 
                        x='Season', 
                        y=['Recency', 'Frequency', 'Average_Rentals'],
                        title='RFM Metrics by Season',
                        barmode='group')
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col2:
        # Normalized RFM metrics
        scaler = MinMaxScaler()
        normalized_data = rfm_data.copy()
        normalized_data[['Recency', 'Frequency', 'Average_Rentals']] = scaler.fit_transform(
            rfm_data[['Recency', 'Frequency', 'Average_Rentals']])

        fig_norm_rfm = px.line(normalized_data, 
                              x='Season', 
                              y=['Recency', 'Frequency', 'Average_Rentals'],
                              title='Normalized RFM Metrics')
        st.plotly_chart(fig_norm_rfm, use_container_width=True)

# Tab 3: Segmentation
with tab3:
    st.subheader("Customer Segmentation Analysis")

    # Create segments based on rental patterns
    daily_df['rental_segment'] = pd.qcut(daily_df['cnt'], 
                                       q=4, 
                                       labels=['Low', 'Medium', 'High', 'Very High'])

    # Segment analysis
    col1, col2 = st.columns(2)

    with col1:
        # Average rentals by segment
        segment_avg = daily_df.groupby('rental_segment', observed=False)['cnt'].mean().reset_index()
        fig_segment = px.bar(segment_avg, 
                           x='rental_segment', 
                           y='cnt',
                           title='Average Daily Rentals by Segment')
        st.plotly_chart(fig_segment, use_container_width=True)

    with col2:
        # User composition by segment
        segment_composition = daily_df.groupby('rental_segment', observed=False)[['casual', 'registered']].mean().reset_index()
        fig_composition = px.bar(segment_composition, 
                               x='rental_segment', 
                               y=['casual', 'registered'],
                               title='User Composition by Segment',
                               barmode='stack')
        st.plotly_chart(fig_composition, use_container_width=True)

    # Additional segment insights
    col1, col2 = st.columns(2)

    with col1:
        # Seasonal distribution within segments
        seasonal_dist = pd.crosstab(daily_df['rental_segment'], daily_df['season'])
        fig_seasonal_dist = px.bar(seasonal_dist, 
                                 title='Seasonal Distribution by Segment',
                                 barmode='stack')
        st.plotly_chart(fig_seasonal_dist, use_container_width=True)

    with col2:
        # Weather conditions by segment
        weather_dist = pd.crosstab(daily_df['rental_segment'], 
                                 daily_df['weathersit'], 
                                 normalize='index') * 100
        fig_weather_dist = px.bar(weather_dist, 
                                title='Weather Conditions by Segment (%)',
                                barmode='stack')
        st.plotly_chart(fig_weather_dist, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created by Ikhwananda | Data Source: Bike Sharing Dataset")