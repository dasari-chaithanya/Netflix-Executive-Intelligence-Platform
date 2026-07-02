import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw Netflix dataset.
    Returns the Bronze -> Silver transitional dataframe.
    """
    logger.info("Starting data cleaning (Raw -> Silver)")
    df_clean = df.copy()
    
    # 1. Standardize text columns (strip whitespace)
    text_cols = ['title', 'director', 'cast', 'country', 'listed_in', 'description']
    for col in text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('nan', None)
            df_clean[col] = df_clean[col].replace('None', None)
            df_clean[col] = df_clean[col].replace('', None)
            
    # 2. Impute specific nulls
    # Director and Cast are reasonably 'Unknown' if missing
    if 'director' in df_clean.columns:
        df_clean['director'] = df_clean['director'].fillna('Unknown')
    if 'cast' in df_clean.columns:
        df_clean['cast'] = df_clean['cast'].fillna('Unknown')
        
    # We do NOT impute Country with 'Unknown' as per explicit instructions.
    # Leave country nulls intact for accurate geographic analysis.
    
    # 3. Parse Dates
    if 'date_added' in df_clean.columns:
        df_clean['date_added'] = pd.to_datetime(df_clean['date_added'].str.strip(), format='mixed', errors='coerce')
        
    # 4. Standardize Ratings
    if 'rating' in df_clean.columns:
        # Some durations were accidentally placed in the rating column in the raw Kaggle dataset.
        invalid_ratings = ['74 min', '84 min', '66 min']
        
        # Move misaligned durations back to duration column
        mask = df_clean['rating'].isin(invalid_ratings)
        df_clean.loc[mask, 'duration'] = df_clean.loc[mask, 'rating']
        df_clean.loc[mask, 'rating'] = None
        
        # Standardize missing/unrated to 'NR'
        df_clean['rating'] = df_clean['rating'].fillna('NR')
        df_clean['rating'] = df_clean['rating'].replace({'UR': 'NR'})
        
    logger.info("Data cleaning completed.")
    return df_clean
