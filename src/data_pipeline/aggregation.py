import pandas as pd

def aggregate_country_genre_counts(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Aggregates volume by country and genre combinations.
    Useful for heavy maps and matrix charts to avoid exploding on the fly.
    \"\"\"
    if 'countries' not in df.columns or 'genres' not in df.columns:
        return pd.DataFrame()
        
    # Explode countries, then genres
    df_exp = df.explode('countries').explode('genres')
    
    # Drop unknowns
    df_exp = df_exp[df_exp['countries'] != 'Unknown']
    
    agg = df_exp.groupby(['countries', 'genres']).size().reset_index(name='Total Titles')
    return agg
