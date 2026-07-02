import pandas as pd

def get_top_countries(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Returns the top N countries by total titles produced."""
    if 'countries' not in df.columns:
        return pd.DataFrame()
        
    # Explode the lists
    exploded = df.explode('countries')
    exploded = exploded[exploded['countries'] != 'Unknown']
    
    top = exploded['countries'].value_counts().head(top_n).reset_index()
    top.columns = ['Country', 'Total Titles']
    return top
