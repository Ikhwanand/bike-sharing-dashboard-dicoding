# Bike Sharing Dashboard

## Project Description
This project is a comprehensive data analysis of a bike-sharing system, exploring rental patterns, user behaviors, and environmental influences on bike usage.

## Background
Bike-sharing systems represent a modern approach to urban transportation, providing automated bike rental services. This project aims to uncover insights from a rich dataset of bike rentals, examining how factors like weather, time, and user type impact bike usage.

## Dataset Overview
- **Hourly Data**: 17,379 entries tracking bike rentals by hour
- **Daily Data**: 731 entries summarizing daily bike rental statistics
- **Key Features**: 
  - Temporal analysis
  - Weather impact
  - Seasonal variations
  - User type breakdown

## Project Structure
- `data/`: Contains source datasets
- [EDA.ipynb](cci:7://file:///d:/dashboard-submit-dicoding/EDA.ipynb:0:0-0:0): Exploratory Data Analysis Jupyter notebook
- [requirements.txt](cci:7://file:///d:/dashboard-submit-dicoding/requirements.txt:0:0-0:0): Project dependencies

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps
1. Clone the repository
```bash
git clone https://github.com/yourusername/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the dashboard
```bash
streamlit run ./dashboard/app.py
```


### Key Libraries
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
### Main Insights
* Analyze bike rental patterns across different:
** Seasons
** Weather conditions
** Time of day
** User types (casual vs. registered)

### Contributing
Contributions are welcome! Please submit pull requests or open issues.

