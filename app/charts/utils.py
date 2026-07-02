import plotly.graph_objects as go
import pandas as pd
from typing import Optional

def validate_chart_data(df: pd.DataFrame, required_cols: list[str]) -> bool:
    """Checks if a dataframe is valid and has required columns."""
    if df is None or df.empty:
        return False
    for col in required_cols:
        if col not in df.columns:
            return False
    return True

def create_empty_chart(message: str = "No data available") -> go.Figure:
    """Returns a blank figure with a text message."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#666")
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    return fig
