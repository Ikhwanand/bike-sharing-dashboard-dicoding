import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    hourly_df = pd.read_csv('../data/hour.csv')
    daily_df = pd.read_csv('../data/day.csv')
    
    # Convert datetime
    hourly_df['dteday'] = pd.to_datetime(hourly_df['dteday'])
    daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
    
    return hourly_df, daily_df

# Load the data
hourly_df, daily_df = load_data()

# Title
st.title("🚲 Bike Sharing Dashboard")

# Sidebar
st.sidebar.header("Filters")
# Add date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [daily_df['dteday'].min(), daily_df['dteday'].max()]
)

hourly_df = hourly_df[(hourly_df['dteday'] >= str(date_range[0])) & (hourly_df['dteday'] <= str(date_range[1]))]
daily_df = daily_df[(daily_df['dteday'] >= str(date_range[0])) & (daily_df['dteday'] <= str(date_range[1]))]

# Main KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rentals", f"{daily_df['cnt'].sum():,}")
with col2:
    st.metric("Average Daily Rentals", f"{daily_df['cnt'].mean():.0f}")
with col3:
    st.metric("Casual Users", f"{(hourly_df['casual'].sum() / hourly_df['cnt'].sum() * 100):.1f}%")
with col4:
    st.metric("Registered Users", f"{(hourly_df['registered'].sum() / hourly_df['cnt'].sum() * 100):.1f}%")

# Create tabs for different visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Temporal Analysis", "Weather Impact", "User Analysis", 'RFM Analysis'])

with tab1:
    # Daily trend
    st.subheader("Daily Rental Trend")
    fig_daily = px.line(daily_df, x='dteday', y='cnt', 
                       title='Daily Bike Rentals Over Time')
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Hourly pattern
    st.subheader("Average Hourly Pattern")
    hourly_pattern = hourly_df.groupby('hr')['cnt'].mean().reset_index()
    fig_hourly = px.line(hourly_pattern, x='hr', y='cnt',
                        title='Average Rentals by Hour of Day')
    st.plotly_chart(fig_hourly, use_container_width=True)

with tab2:
    # Weather impact
    st.subheader("Weather Impact Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_temp = px.scatter(hourly_df, x='temp', y='cnt',
                            title='Temperature vs Rentals')
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        fig_hum = px.scatter(hourly_df, x='hum', y='cnt',
                           title='Humidity vs Rentals')
        st.plotly_chart(fig_hum, use_container_width=True)

with tab3:
    # User type comparison
    st.subheader("User Type Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        user_type_data = pd.DataFrame({
            'Type': ['Casual', 'Registered'],
            'Count': [hourly_df['casual'].sum(), hourly_df['registered'].sum()]
        })
        fig_users = px.pie(user_type_data, values='Count', names='Type',
                          title='Distribution of User Types')
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        # Weekday vs Weekend comparison
        weekday_data = hourly_df.groupby('weekday')['cnt'].mean().reset_index()
        fig_weekday = px.bar(weekday_data, x='weekday', y='cnt',
                            title='Average Rentals by Day of Week')
        st.plotly_chart(fig_weekday, use_container_width=True)

with tab4:
    # RFM Analysis
    st.subheader('RFM Analysis')
    
    col1, col2 = st.columns(2)

    with col1:
        # First, let's get the last date in our dataset
        last_date = daily_df['dteday'].max()

        # Calculate RFM metrics
        rfm_df = pd.DataFrame()

        # Recency: Days since last rental
        rfm_df['Recency'] = (last_date - daily_df['dteday']).dt.days

        # Frequency: We'll use the count of rentals per day
        rfm_df['Frequency'] = daily_df['cnt']

        # Monetary: Total bikes rented (we'll use the same as frequency since we don't have price data)
        rfm_df['Monetary'] = daily_df['cnt']

        # Create R, F, M segments
        r_labels = range(4, 0, -1)
        r_quartiles = pd.qcut(rfm_df['Recency'], q=4, labels=r_labels)
        f_labels = range(1, 5)
        f_quartiles = pd.qcut(rfm_df['Frequency'], q=4, labels=f_labels)
        m_labels = range(1, 5)
        m_quartiles = pd.qcut(rfm_df['Monetary'], q=4, labels=m_labels)

        # Create new columns for the segments
        rfm_df['R'] = r_quartiles
        rfm_df['F'] = f_quartiles
        rfm_df['M'] = m_quartiles

        # Calculate RFM score 
        rfm_df['RFM_Score'] = rfm_df['R'].astype(str) + rfm_df['F'].astype(str) + rfm_df['M'].astype(str)

        # Create segment labels
        def segment_customers(row):
            if row['R'] >= 3 and row['F'] >= 3 and row['M'] >= 3:
                return 'Best Customers'
            elif row['R'] >= 3 and row['F'] >= 3:
                return 'Loyal Customers'
            elif row['R'] >= 3:
                return 'Recent Customers'
            elif row['F'] >= 3 and row['M'] >= 3:
                return 'High Value'
            else:
                return 'Lost Customers'

        rfm_df['Customer_Segment'] = rfm_df.apply(segment_customers, axis=1)

        fig = px.pie(
        rfm_df,
        names='Customer_Segment',
        title='Customer Segmentation Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3  # Use Set3 colormap
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    with col2:
        st.subheader('Top 10 Customers by RFM Score')
        st.dataframe(rfm_df.sort_values('RFM_Score', ascending=False).head(10))

# Footer
st.markdown("---")
st.markdown("Dashboard created by Ikhwananda | Data Source: Bike Sharing Dataset")