import plotly.graph_objects as go
from app.charts.theme import get_chart_theme_layout
from app.theme.provider import theme_provider

class BaseChartBuilder:
    """Base class for all chart builders."""
    
    def __init__(self, df, title: str = None):
        self.df = df
        self.title = title
        self.fig = go.Figure()
        self.primary_color = theme_provider.get_color("brand", "red")
        self.secondary_color = theme_provider.get_color("chart", "primary")

    def _apply_theme(self):
        """Applies global theming."""
        layout = get_chart_theme_layout()
        if self.title:
            layout["title"] = {"text": self.title, "x": 0.05, "xanchor": "left"}
        self.fig.update_layout(**layout)
        # Custom Modebar (Download PNG/CSV, Fullscreen, Reset)
        self.fig.update_layout(modebar_add=["v1hovermode", "toggleSpikelines"])

    def build(self) -> go.Figure:
        """To be implemented by subclasses."""
        raise NotImplementedError
