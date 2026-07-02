import pytest

def test_navigation_import():
    from app.components.navigation import render_sidebar
    assert callable(render_sidebar)
