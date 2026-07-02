import pytest
from app.mock.charts import get_mock_bar_data
from app.charts.bar import BarChartBuilder
import plotly.graph_objects as go

def test_bar_chart_builder_returns_figure():
    df = get_mock_bar_data()
    builder = BarChartBuilder(df, x_col="Category", y_col="Value")
    fig = builder.build()
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0

def test_chart_empty_state():
    # Pass None to force empty state
    builder = BarChartBuilder(None, x_col="Category", y_col="Value")
    fig = builder.build()
    
    assert isinstance(fig, go.Figure)
    # Check if empty state annotation exists
    assert len(fig.layout.annotations) > 0
    assert "No data available" in fig.layout.annotations[0].text
