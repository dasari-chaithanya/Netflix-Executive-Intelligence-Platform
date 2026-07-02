import plotly.express as px
from app.charts.base import BaseChartBuilder
from app.charts.utils import validate_chart_data, create_empty_chart

class LineChartBuilder(BaseChartBuilder):
    def __init__(self, df, x_col: str, y_cols: list, title: str = None, area: bool = False):
        super().__init__(df, title)
        self.x_col = x_col
        self.y_cols = y_cols
        self.area = area

    def build(self) -> go.Figure:
        if not validate_chart_data(self.df, [self.x_col] + self.y_cols):
            return create_empty_chart()
            
        self.fig = px.line(
            self.df, 
            x=self.x_col, 
            y=self.y_cols, 
            color_discrete_sequence=[self.primary_color, self.secondary_color]
        )
        
        # Premium updates: Spline curves, markers on hover, subtle area fill
        fill_val = 'tozeroy' if self.area else None
        
        self.fig.update_traces(
            mode='lines',
            line_shape='spline',
            fill=fill_val,
            fillcolor='rgba(229, 9, 20, 0.15)' if self.area else None,
            hoverinfo='all',
            hovertemplate='%{x}<br><b>%{y:.2s}</b><extra></extra>' # Better tooltips
        )
        
        self._apply_theme()
        return self.fig
