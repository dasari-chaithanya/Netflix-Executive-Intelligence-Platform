import pytest
from app.viewmodels.executive import ExecutiveViewModel
from app.viewmodels.content import ContentViewModel
import pandas as pd

# We use the real load_processed_data via the BaseViewModel, but we can mock if needed.
# Since this is an integration test, we expect the parquet file to exist.

def test_executive_view_model():
    vm = ExecutiveViewModel()
    data = vm.get_data()
    
    assert "is_empty" in data
    assert "kpis" in data
    assert "summary" in data
    
    if not data["is_empty"]:
        assert "catalog_freshness" in data["kpis"]
        assert "average_content_age" in data["kpis"]

def test_content_view_model():
    vm = ContentViewModel()
    data = vm.get_data()
    
    assert "is_empty" in data
    if not data["is_empty"]:
        assert "distribution_df" in data
        assert isinstance(data["distribution_df"], pd.DataFrame)
        assert "trend_df" in data
