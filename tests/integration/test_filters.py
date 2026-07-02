import pytest
import pandas as pd
from app.data.filters import apply_global_filters

def test_apply_global_filters_content_type():
    df = pd.DataFrame({
        "type": ["Movie", "Movie", "TV Show", "Movie"],
        "release_year": [2020, 2021, 2021, 2022],
        "genres": ["Action", "Drama", "Action", "Comedy"],
        "country": ["USA", "India", "USA", "UK"]
    })
    
    filters = {
        "content_type": "Movie"
    }
    
    filtered = apply_global_filters(df, filters)
    assert len(filtered) == 3
    assert all(filtered["type"] == "Movie")

def test_apply_global_filters_release_year():
    df = pd.DataFrame({
        "type": ["Movie", "Movie", "TV Show", "Movie"],
        "release_year": [2020, 2021, 2021, 2022],
        "genres": ["Action", "Drama", "Action", "Comedy"],
        "country": ["USA", "India", "USA", "UK"]
    })
    
    filters = {
        "release_year": (2021, 2022)
    }
    
    filtered = apply_global_filters(df, filters)
    assert len(filtered) == 3
    assert 2020 not in filtered["release_year"].values

def test_apply_global_filters_genres():
    df = pd.DataFrame({
        "type": ["Movie", "Movie", "TV Show", "Movie"],
        "release_year": [2020, 2021, 2021, 2022],
        "genres": ["Action, Thriller", "Drama", "Action", "Comedy"],
        "country": ["USA", "India", "USA", "UK"]
    })
    
    filters = {
        "genres": ["Action"]
    }
    
    filtered = apply_global_filters(df, filters)
    assert len(filtered) == 2
