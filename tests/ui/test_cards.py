import pytest

def test_cards_import():
    from app.components.cards import kpi_card
    assert callable(kpi_card)
