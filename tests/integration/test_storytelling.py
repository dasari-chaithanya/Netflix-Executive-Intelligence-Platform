import pytest
from app.business.storytelling import generate_executive_summary, generate_insight, generate_recommendation
from app.business.rules import get_status_color

def test_generate_executive_summary():
    mock_kpis = {
        "catalog_freshness": {"value": 45.0},
        "average_content_age": {"value": 3.2}
    }
    
    summary = generate_executive_summary(mock_kpis)
    assert "healthy" in summary
    assert "45.0%" in summary
    assert "3.2 years" in summary

def test_generate_insight_green():
    insight = generate_insight("catalog_freshness", 40.0, "Testing context")
    assert "Strong Catalog Freshness" in insight["title"]
    assert "Testing context" in insight["text"]

def test_generate_recommendation_red():
    # Value 10 is way below 35 or 25, should trigger red/shift
    status = get_status_color("catalog_freshness", 10.0)
    rec = generate_recommendation(status, "Content Acquisition")
    assert status == "red"
    assert "Shift Investment" in rec["title"]
