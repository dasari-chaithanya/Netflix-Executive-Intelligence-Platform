import pytest
import pandas as pd
from src.analytics_engine.overview import get_content_type_distribution
from src.analytics_engine.countries import get_top_countries

def test_content_type_distribution():
    df = pd.DataFrame({'type': ['Movie', 'Movie', 'TV Show']})
    dist = get_content_type_distribution(df)
    assert dist[dist['Content Type'] == 'Movie']['Total Titles'].iloc[0] == 2
    assert dist[dist['Content Type'] == 'TV Show']['Total Titles'].iloc[0] == 1

def test_top_countries():
    df = pd.DataFrame({'countries': [['USA', 'UK'], ['USA'], ['India']]})
    top = get_top_countries(df)
    assert len(top) == 3
    assert top[top['Country'] == 'USA']['Total Titles'].iloc[0] == 2
