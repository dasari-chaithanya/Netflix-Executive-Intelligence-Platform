import pandas as pd

def get_mature_audience_share(df: pd.DataFrame) -> float:
    """
    Calculates the Mature Audience Share %.
    Formula: (Titles rated TV-MA, R, NC-17) / (Total Titles)
    """
    if 'rating' not in df.columns:
        raise ValueError("DataFrame must contain 'rating' column.")
        
    mature_ratings = ['TV-MA', 'R', 'NC-17']
    mature_titles = df[df['rating'].isin(mature_ratings)]
    
    if len(df) == 0:
        return 0.0
        
    return (len(mature_titles) / len(df)) * 100
