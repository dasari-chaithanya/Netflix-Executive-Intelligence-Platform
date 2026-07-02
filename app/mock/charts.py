import pandas as pd
import numpy as np

def get_mock_bar_data() -> pd.DataFrame:
    return pd.DataFrame({
        "Category": ["United States", "India", "United Kingdom", "Japan", "South Korea"],
        "Value": [3500, 1000, 800, 600, 500]
    })

def get_mock_line_data() -> pd.DataFrame:
    years = list(range(2015, 2025))
    return pd.DataFrame({
        "Year": years,
        "Movies": np.random.randint(200, 800, len(years)),
        "TV Shows": np.random.randint(100, 500, len(years))
    })

def get_mock_map_data() -> pd.DataFrame:
    return pd.DataFrame({
        "Country": ["USA", "IND", "GBR", "JPN", "KOR", "FRA", "CAN", "ESP"],
        "Volume": [3500, 1000, 800, 600, 500, 400, 300, 250]
    })

def get_mock_heatmap_data() -> pd.DataFrame:
    genres = ["Drama", "Comedy", "Action", "Documentary"]
    years = ["2020", "2021", "2022", "2023"]
    
    data = []
    for g in genres:
        for y in years:
            data.append({"Genre": g, "Year": y, "Count": np.random.randint(50, 300)})
            
    return pd.DataFrame(data)
