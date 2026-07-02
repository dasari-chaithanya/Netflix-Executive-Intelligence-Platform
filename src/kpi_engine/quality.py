import pandas as pd

def get_series_survival_rate(df: pd.DataFrame) -> float:
    """
    Calculates the Series Survival Rate %.
    Formula: (TV Shows with > 1 Season) / (Total TV Shows)
    """
    if 'type' not in df.columns or 'duration_seasons' not in df.columns:
        raise ValueError("DataFrame must contain 'type' and 'duration_seasons' columns.")
        
    tv_shows = df[df['type'] == 'TV Show']
    
    if len(tv_shows) == 0:
        return 0.0
        
    surviving_shows = tv_shows[tv_shows['duration_seasons'] > 1]
    
    return (len(surviving_shows) / len(tv_shows)) * 100
