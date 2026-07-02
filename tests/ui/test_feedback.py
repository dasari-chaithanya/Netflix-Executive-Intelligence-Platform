import pytest

def test_feedback_import():
    from app.components.feedback import empty_state
    assert callable(empty_state)
