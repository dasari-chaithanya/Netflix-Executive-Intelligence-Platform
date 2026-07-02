import pytest

def test_layout_import():
    from app.components.layout import section_header
    assert callable(section_header)
