import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    hourly_df = pd.read_csv('./data/hour.csv')
    daily_df = pd.read_csv('./data/day.csv')
    
    # Convert datetime
    hourly_df['dteday'] = pd.to_datetime(hourly_df['dteday'])
    daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
    
    # Create season mapping
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    hourly_df['season_name'] = hourly_df['season'].map(season_map)
    daily_df['season_name'] = daily_df['season'].map(season_map)
    
    return hourly_df, daily_df

# Load data
hourly_df, daily_df = load_data()

# Title and description
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Analysis of bike sharing patterns and trends")

# Sidebar filters
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date",
    min_value=daily_df['dteday'].min(),
    max_value=daily_df['dteday'].max(),
    value=[daily_df['dteday'].min(), daily_df['dteday'].max()]
)

hourly_df = hourly_df[(hourly_df['dteday'] >= str(selected_date[0])) & (hourly_df['dteday'] <= str(selected_date[1]))]
daily_df = daily_df[(daily_df['dteday'] >= str(selected_date[0])) & (daily_df['dteday'] <= str(selected_date[1]))]

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rentals", f"{hourly_df['cnt'].sum():,}")
with col2:
    st.metric("Average Daily Rentals", f"{daily_df['cnt'].mean():.0f}")
with col3:
    st.metric("Casual Users", f"{hourly_df['casual'].sum():,}")
with col4:
    st.metric("Registered Users", f"{hourly_df['registered'].sum():,}")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Usage Patterns", "Weather Impact", "User Analysis", 'Customer Segmentation'])

with tab1:
    st.header("Usage Patterns")
    
    # Hourly pattern
    hourly_pattern = hourly_df.groupby('hr')['cnt'].mean()
    fig_hourly = px.line(
        x=hourly_pattern.index,
        y=hourly_pattern.values,
        title="Average Rentals by Hour",
        labels={'x': 'Hour of Day', 'y': 'Average Rentals'}
    )
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Seasonal pattern
    seasonal_pattern = hourly_df.groupby('season_name')['cnt'].mean()
    fig_seasonal = px.bar(
        x=seasonal_pattern.index,
        y=seasonal_pattern.values,
        title="Average Rentals by Season",
        labels={'x': 'Season', 'y': 'Average Rentals'}
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)

with tab2:
    st.header("Weather Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature vs Rentals
        fig_temp = px.scatter(
            hourly_df,
            x='temp',
            y='cnt',
            title="Temperature vs Rentals",
            labels={'temp': 'Temperature', 'cnt': 'Number of Rentals'}
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Humidity vs Rentals
        fig_hum = px.scatter(
            hourly_df,
            x='hum',
            y='cnt',
            title="Humidity vs Rentals",
            labels={'hum': 'Humidity', 'cnt': 'Number of Rentals'}
        )
        st.plotly_chart(fig_hum, use_container_width=True)

with tab3:
    st.header("User Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # User type distribution
        user_data = pd.DataFrame({
            'Type': ['Casual', 'Registered'],
            'Count': [hourly_df['casual'].sum(), hourly_df['registered'].sum()]
        })
        fig_users = px.pie(
            user_data,
            values='Count',
            names='Type',
            title="Distribution of User Types"
        )
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        # Weekly pattern by user type
        weekly_pattern = hourly_df.groupby('weekday')[['casual', 'registered']].mean()
        fig_weekly = px.line(
            weekly_pattern,
            title="Weekly Pattern by User Type",
            labels={'weekday': 'Day of Week', 'value': 'Average Rentals'}
        )
        st.plotly_chart(fig_weekly, use_container_width=True)


with tab4:
    # Calculate RFM metrics
    last_date = hourly_df['dteday'].max()

    # Group by date to get daily metrics
    daily_metrics = hourly_df.groupby('dteday').agg({
        'cnt': 'sum',  # Total rentals per day
        'casual': 'sum',  # Casual users per day
        'registered': 'sum'  # Registered users per day
    }).reset_index()

    # Calculate RFM scores
    rfm_data = pd.DataFrame()

    # Recency (days since last rental)
    rfm_data['Recency'] = (last_date - daily_metrics['dteday']).dt.days

    # Frequency (number of rentals)
    rfm_data['Frequency'] = daily_metrics['cnt']

    # Monetary (using total rentals as proxy since we don't have actual monetary values)
    rfm_data['Monetary'] = daily_metrics['cnt']

    # Create R, F, M quartiles
    r_labels = range(4, 0, -1)  # 4 is best, 1 is worst
    f_labels = range(1, 5)  # 1 is worst, 4 is best
    m_labels = range(1, 5)  # 1 is worst, 4 is best

    r_quartiles = pd.qcut(rfm_data['Recency'], q=4, labels=r_labels)
    f_quartiles = pd.qcut(rfm_data['Frequency'], q=4, labels=f_labels)
    m_quartiles = pd.qcut(rfm_data['Monetary'], q=4, labels=m_labels)

    # Create new columns for the quartiles
    rfm_data['R'] = r_quartiles
    rfm_data['F'] = f_quartiles
    rfm_data['M'] = m_quartiles

    # Calculate RFM Score
    rfm_data['RFM_Score'] = rfm_data['R'].astype(str) + rfm_data['F'].astype(str) + rfm_data['M'].astype(str)

    # Create segment labels
    def segment_customers(row):
        if row['R'] >= 3 and row['F'] >= 3 and row['M'] >= 3:
            return 'Best Days'
        elif row['R'] >= 3 and row['F'] >= 3:
            return 'Loyal Days'
        elif row['R'] >= 3:
            return 'Recent Days'
        elif row['F'] >= 3 and row['M'] >= 3:
            return 'High Value Days'
        else:
            return 'Lost Days'

    rfm_data['Customer_Segment'] = rfm_data.apply(segment_customers, axis=1)

    # Visualize segments
    segment_counts = rfm_data['Customer_Segment'].value_counts()
    fig = px.bar(
        segment_counts,
        x=segment_counts.index,
        y=segment_counts.values,
        labels={'x': 'Segment', 'y': 'Number of Days'},
        title='Distribution of Day Segments'
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created for Bike Sharing Analysis")