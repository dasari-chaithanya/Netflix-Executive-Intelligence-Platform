import pandas as pd

def get_rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the distribution of maturity ratings."""
    if 'rating' not in df.columns:
        return pd.DataFrame()
        
    dist = df['rating'].value_counts().reset_index()
    dist.columns = ['Rating', 'Total Titles']
    return dist
