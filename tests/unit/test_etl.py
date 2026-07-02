import pytest
import pandas as pd
from src.data_pipeline.cleaning import clean_data
from src.data_pipeline.feature_engineering import engineer_features

def test_clean_data():
    raw = pd.DataFrame({
        'title': ['  Movie 1  ', 'Movie 2'],
        'director': [None, 'John Doe'],
        'rating': ['74 min', 'UR']
    })
    
    cleaned = clean_data(raw)
    
    assert cleaned['title'].iloc[0] == 'Movie 1'
    assert cleaned['director'].iloc[0] == 'Unknown'
    assert cleaned['rating'].iloc[1] == 'NR'
    assert cleaned['rating'].iloc[0] == 'NR' # 74 min moved to duration, then null filled with NR
    assert cleaned['duration'].iloc[0] == '74 min'

def test_engineer_features():
    silver = pd.DataFrame({
        'type': ['Movie', 'TV Show'],
        'duration': ['90 min', '3 Seasons'],
        'listed_in': ['Action, Thriller', 'Drama'],
        'release_year': [2015, 2021],
        'date_added': pd.to_datetime(['2016-01-01', '2022-01-01'])
    })
    
    gold = engineer_features(silver)
    
    assert gold['duration_mins'].iloc[0] == 90
    assert pd.isna(gold['duration_seasons'].iloc[0])
    
    assert pd.isna(gold['duration_mins'].iloc[1])
    assert gold['duration_seasons'].iloc[1] == 3
    
    assert gold['genres'].iloc[0] == ['Action', 'Thriller']
    assert gold['genre_count'].iloc[0] == 2
    
    assert gold['release_decade'].iloc[0] == 2010
