import pytest

def test_filters_import():
    from app.components.filters import global_filter_panel
    assert callable(global_filter_panel)
