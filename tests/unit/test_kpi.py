import pytest
import pandas as pd
from datetime import datetime
from src.kpi_engine.catalog import get_catalog_freshness, get_average_content_age
from src.kpi_engine.quality import get_series_survival_rate

def test_catalog_freshness():
    df = pd.DataFrame({
        'date_added': pd.to_datetime(['2023-01-01', '2022-01-01', '2019-01-01'])
    })
    # Mock 'Today' as 2023-06-01
    freshness = get_catalog_freshness(df, reference_date=pd.to_datetime('2023-06-01'))
    # Last 24 months from 2023-06-01 is 2021-06-01. So 2023-01 and 2022-01 are fresh.
    assert freshness == (2 / 3) * 100

def test_average_content_age():
    df = pd.DataFrame({'release_year': [2010, 2020]})
    age = get_average_content_age(df, current_year=2024)
    assert age == 9.0 # (14 + 4) / 2

def test_series_survival_rate():
    df = pd.DataFrame({
        'type': ['TV Show', 'TV Show', 'Movie'],
        'duration_seasons': [1, 3, None]
    })
    survival = get_series_survival_rate(df)
    assert survival == 50.0 # 1 out of 2 tv shows
