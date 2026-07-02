import pandas as pd

def get_content_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the count of Titles by Content Type (Movie vs TV Show)."""
    if 'type' not in df.columns:
        return pd.DataFrame()
        
    dist = df['type'].value_counts().reset_index()
    dist.columns = ['Content Type', 'Total Titles']
    return dist
