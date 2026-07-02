import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_catalog_freshness(df: pd.DataFrame, reference_date: datetime = None) -> float:
    """
    Calculates Catalog Freshness %.
    Formula: (Titles added in the last 24 months) / (Total Titles)
    """
    if 'date_added' not in df.columns:
        raise ValueError("DataFrame must contain 'date_added' column.")
        
    if reference_date is None:
        # Use the max date in the dataset to simulate "Today" for a static dataset
        reference_date = df['date_added'].max()
        if pd.isna(reference_date):
            return 0.0
            
    cutoff_date = reference_date - relativedelta(months=24)
    recent_titles = df[df['date_added'] >= cutoff_date]
    
    if len(df) == 0:
        return 0.0
        
    return (len(recent_titles) / len(df)) * 100

def get_average_content_age(df: pd.DataFrame, current_year: int = None) -> float:
    """
    Calculates Average Content Age in years.
    Formula: Mean(Current_Year - Release_Year)
    """
    if 'release_year' not in df.columns:
        raise ValueError("DataFrame must contain 'release_year' column.")
        
    if current_year is None:
        current_year = datetime.now().year
        
    if len(df) == 0:
        return 0.0
        
    ages = current_year - df['release_year']
    return float(ages.mean())
