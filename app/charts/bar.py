import plotly.express as px
from app.charts.base import BaseChartBuilder
from app.charts.utils import validate_chart_data, create_empty_chart

class BarChartBuilder(BaseChartBuilder):
    def __init__(self, df, x_col: str, y_col: str, title: str = None, horizontal: bool = False):
        super().__init__(df, title)
        self.x_col = x_col
        self.y_col = y_col
        self.horizontal = horizontal

    def build(self):
        if not validate_chart_data(self.df, [self.x_col, self.y_col]):
            return create_empty_chart()

        # Dummy implementation for UI structure
        orientation = 'h' if self.horizontal else 'v'
        
        self.fig = px.bar(
            self.df, 
            x=self.x_col if not self.horizontal else self.y_col, 
            y=self.y_col if not self.horizontal else self.x_col, 
            orientation=orientation,
            color_discrete_sequence=[self.primary_color]
        )
        self.fig.update_traces(hovertemplate='%{x}<br><b>%{y:.2s}</b><extra></extra>')
        self._apply_theme()
        return self.fig
