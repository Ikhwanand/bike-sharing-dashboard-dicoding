# Bike Sharing Dashboard 🚲

## Overview
This project is a **Streamlit-based dashboard** for analyzing bike sharing patterns and trends. It provides insights into rental behaviors, user types, weather impact, and seasonal trends using interactive visualizations.

## Features
- **Temporal Analysis**: Hourly, daily, and weekly rental patterns.
- **Weather Impact**: How weather conditions affect bike rentals.
- **User Type Analysis**: Distribution of casual vs registered users.
- **Seasonal Analysis**: Rental trends across different seasons.
- **Interactive Filters**: Filter data by year, season, and other parameters.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/bike-sharing-dashboard.git
   ```

2. Navigate to the project directory:
  ```bash
  cd bike-sharing-dashboard
  ```

3. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. Run the Streamlit app:
  ```bash
  streamlit run dashboard/app.py
  ```

2. Open your browser and navigate to `http://localhost:8501`


### Data

The dataset used in this project is the Bike Sharing Dataset from Dicoding. It includes:

* Hourly data: hour.csv
* Daily data: day.csv

### Technologies

* Python: Primary programming language.
* Streamlit: Framework for building the dashboard.
* Plotly: Library for creating interactive visualizations.
* Pandas: Data manipulation and analysis.