import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def extract_duration(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts duration into minutes (for movies) and seasons (for TV shows)."""
    df_feat = df.copy()
    
    if 'duration' in df_feat.columns:
        # Extract numeric part
        dur_numeric = df_feat['duration'].str.extract('(\d+)').astype(float)
        
        # Create separate columns based on type
        is_movie = df_feat['type'] == 'Movie'
        is_tv = df_feat['type'] == 'TV Show'
        
        df_feat['duration_mins'] = np.where(is_movie, dur_numeric[0], np.nan)
        df_feat['duration_seasons'] = np.where(is_tv, dur_numeric[0], np.nan)
        
    return df_feat

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers new features from the Silver dataset.
    Returns the Silver -> Gold dataset.
    """
    logger.info("Starting feature engineering (Silver -> Gold)")
    df_feat = df.copy()
    
    # 1. Extract Durations
    df_feat = extract_duration(df_feat)
    
    # 2. Explode Lists (Store as actual Python lists, not strings)
    if 'listed_in' in df_feat.columns:
        df_feat['genres'] = df_feat['listed_in'].apply(
            lambda x: [g.strip() for g in str(x).split(',')] if pd.notna(x) else []
        )
        df_feat['genre_count'] = df_feat['genres'].apply(len)
        
    if 'country' in df_feat.columns:
        df_feat['countries'] = df_feat['country'].apply(
            lambda x: [c.strip() for c in str(x).split(',')] if pd.notna(x) else []
        )
        df_feat['country_count'] = df_feat['countries'].apply(len)
        
    if 'director' in df_feat.columns:
        df_feat['director_list'] = df_feat['director'].apply(
            lambda x: [d.strip() for d in str(x).split(',')] if pd.notna(x) and x != 'Unknown' else []
        )
        df_feat['director_count'] = df_feat['director_list'].apply(len)
        
    if 'cast' in df_feat.columns:
        df_feat['cast_list'] = df_feat['cast'].apply(
            lambda x: [c.strip() for c in str(x).split(',')] if pd.notna(x) and x != 'Unknown' else []
        )
        df_feat['cast_count'] = df_feat['cast_list'].apply(len)
        
    # 3. Time Features
    if 'release_year' in df_feat.columns:
        df_feat['release_decade'] = (df_feat['release_year'] // 10) * 10
        current_year = pd.Timestamp.now().year
        df_feat['catalog_age'] = current_year - df_feat['release_year']
        
    if 'date_added' in df_feat.columns:
        df_feat['month_added'] = df_feat['date_added'].dt.month
        df_feat['year_added'] = df_feat['date_added'].dt.year
        df_feat['weekday_added'] = df_feat['date_added'].dt.day_name()
        
    # Drop intermediate columns if desired, but keeping them is fine for Gold
    logger.info("Feature engineering completed.")
    return df_feat
