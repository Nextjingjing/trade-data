# Project: Trade Data Analysis & Visualization

## 📌 Overview
This project fetches trade data from an API, stores it in an SQLite database, and visualizes it using bar race charts and other statistical analysis.

## 📂 Project Structure
```
project_root/
│-- data/               # Stores database & raw data
│   │-- trade_data.db   # SQLite database
│-- scripts/            # Python scripts for data processing & visualization
│   │-- fetch_data.py   # Fetches data from API & stores in SQLite
│   │-- process_data.py # Cleans & processes data
│   │-- visualize.py    # Generates bar race chart & other plots
│-- visuals/            # Stores output graphs and reports
│   │-- charts/         # Contains bar race charts
│   │-- reports/        # Data analysis reports
│-- notebooks/          # Jupyter Notebooks for analysis
│   │-- analysis.ipynb  # Exploratory data analysis
│-- README.md           # Project documentation
│-- requirements.txt    # Python dependencies
```

## 📥 Installation
Make sure you have **Python 3.8+** installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

## 🔄 Fetching Data
Run the script to fetch data from the API and store it in SQLite:
```bash
python scripts/fetch_data.py
```

## 📊 Data Visualization
Generate a **bar race chart** to visualize trade data trends over time:
```bash
python scripts/visualize.py
```

## 📖 Jupyter Notebook Analysis
To explore the dataset interactively, run:
```bash
jupyter notebook notebooks/analysis.ipynb
```

## 📌 Dependencies
All necessary packages are listed in `requirements.txt`, including:
- `requests` - API data fetching
- `sqlite3` - Database handling
- `pandas` - Data manipulation
- `matplotlib` & `seaborn` - Static data visualization
- `bar_chart_race` - Animated bar race chart
- `jupyter`, `ipython` - Interactive data analysis

## 📜 License
This project is open-source.