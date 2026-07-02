import pandas as pd

def get_top_genres(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Returns the top N genres by total titles."""
    if 'genres' not in df.columns:
        return pd.DataFrame()
        
    exploded = df.explode('genres')
    top = exploded['genres'].value_counts().head(top_n).reset_index()
    top.columns = ['Genre', 'Total Titles']
    return top
