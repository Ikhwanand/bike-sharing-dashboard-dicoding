import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    hourly_df = pd.read_csv('./data/hour.csv')
    daily_df = pd.read_csv('./data/day.csv')
    
    # Convert dteday to datetime
    hourly_df['dteday'] = pd.to_datetime(hourly_df['dteday'])
    daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
    
    # Create season mapping
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {
        1: 'Clear/Few clouds',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    }
    
    hourly_df['season_name'] = hourly_df['season'].map(season_map)
    hourly_df['weather_desc'] = hourly_df['weathersit'].map(weather_map)
    daily_df['season_name'] = daily_df['season'].map(season_map)
    daily_df['weather_desc'] = daily_df['weathersit'].map(weather_map)
    
    return hourly_df, daily_df

hourly_df, daily_df = load_data()

# Title
st.title("🚲 Bike Sharing Dashboard")
st.write("Analysis of bike sharing patterns and trends")

# Sidebar
st.sidebar.header("Dashboard Filters")
selected_year = st.sidebar.selectbox("Select Year", options=[2011, 2012])
selected_season = st.sidebar.multiselect("Select Season", 
                                       options=hourly_df['season_name'].unique(),
                                       default=hourly_df['season_name'].unique())

# Filter data
filtered_hourly = hourly_df[
    (hourly_df['dteday'].dt.year == selected_year) &
    (hourly_df['season_name'].isin(selected_season))
]

# Main metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_rentals = filtered_hourly['cnt'].sum()
    st.metric("Total Rentals", f"{total_rentals:,}")
with col2:
    avg_daily = filtered_hourly.groupby('dteday')['cnt'].sum().mean()
    st.metric("Average Daily Rentals", f"{int(avg_daily):,}")
with col3:
    casual_percent = (filtered_hourly['casual'].sum() / total_rentals * 100)
    st.metric("Casual Users", f"{casual_percent:.1f}%")
with col4:
    registered_percent = (filtered_hourly['registered'].sum() / total_rentals * 100)
    st.metric("Registered Users", f"{registered_percent:.1f}%")

# Charts
st.header("Temporal Analysis")
tab1, tab2, tab3 = st.tabs(["Hourly Patterns", "Weather Impact", "User Types"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly pattern
        hourly_pattern = filtered_hourly.groupby('hr')['cnt'].mean()
        fig_hourly = px.line(hourly_pattern, 
                           title="Average Rentals by Hour",
                           labels={'hr': 'Hour of Day', 'value': 'Average Rentals'})
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        # Daily pattern
        daily_pattern = filtered_hourly.groupby('weekday')['cnt'].mean()
        fig_daily = px.bar(daily_pattern,
                          title="Average Rentals by Day of Week",
                          labels={'weekday': 'Day of Week (0=Sunday)', 'value': 'Average Rentals'})
        st.plotly_chart(fig_daily, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather impact
        fig_weather = px.box(filtered_hourly, x='weather_desc', y='cnt',
                           title="Rental Distribution by Weather",
                           labels={'weather_desc': 'Weather Condition', 'cnt': 'Number of Rentals'})
        st.plotly_chart(fig_weather, use_container_width=True)
    
    with col2:
        # Temperature impact
        fig_temp = px.scatter(filtered_hourly, x='temp', y='cnt',
                            title="Temperature vs Rentals",
                            labels={'temp': 'Temperature (normalized)', 'cnt': 'Number of Rentals'})
        st.plotly_chart(fig_temp, use_container_width=True)

with tab3:
    # User type analysis
    user_type_data = filtered_hourly.groupby('hr')[['casual', 'registered']].mean()
    fig_users = go.Figure()
    fig_users.add_trace(go.Bar(x=user_type_data.index, y=user_type_data['casual'], name='Casual'))
    fig_users.add_trace(go.Bar(x=user_type_data.index, y=user_type_data['registered'], name='Registered'))
    fig_users.update_layout(title="Average Rentals by User Type and Hour",
                          barmode='stack',
                          xaxis_title="Hour of Day",
                          yaxis_title="Average Rentals")
    st.plotly_chart(fig_users, use_container_width=True)

# Seasonal Analysis
st.header("Seasonal Analysis")
seasonal_data = filtered_hourly.groupby('season_name')['cnt'].agg(['mean', 'max', 'min']).round(2)
fig_seasonal = go.Figure()
fig_seasonal.add_trace(go.Bar(x=seasonal_data.index, y=seasonal_data['mean'], name='Average'))
fig_seasonal.add_trace(go.Bar(x=seasonal_data.index, y=seasonal_data['max'], name='Maximum'))
fig_seasonal.add_trace(go.Bar(x=seasonal_data.index, y=seasonal_data['min'], name='Minimum'))
fig_seasonal.update_layout(title="Rental Statistics by Season",
                         barmode='group',
                         xaxis_title="Season",
                         yaxis_title="Number of Rentals")
st.plotly_chart(fig_seasonal, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created by Muhammad Ikhwananda Rizaldi")