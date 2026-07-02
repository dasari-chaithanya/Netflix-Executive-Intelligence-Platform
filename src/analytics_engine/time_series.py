import pandas as pd

def get_monthly_additions(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the count of titles added per month across all years."""
    if 'month_added' not in df.columns:
        return pd.DataFrame()
        
    dist = df['month_added'].value_counts().reset_index()
    dist.columns = ['Month', 'Titles Added']
    dist = dist.sort_values('Month').dropna()
    dist['Month'] = dist['Month'].astype(int)
    return dist
