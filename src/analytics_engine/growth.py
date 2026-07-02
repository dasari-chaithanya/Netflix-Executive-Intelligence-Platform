import pandas as pd

def get_yoy_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the count of titles added per year."""
    if 'year_added' not in df.columns:
        return pd.DataFrame()
        
    growth = df['year_added'].value_counts().reset_index()
    growth.columns = ['Year', 'Titles Added']
    growth = growth.sort_values('Year').dropna()
    growth['Year'] = growth['Year'].astype(int)
    return growth
