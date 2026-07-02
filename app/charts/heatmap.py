import plotly.express as px
from app.charts.base import BaseChartBuilder
from app.charts.utils import validate_chart_data, create_empty_chart

class HeatmapBuilder(BaseChartBuilder):
    def __init__(self, df, x_col: str, y_col: str, val_col: str, title: str = None):
        super().__init__(df, title)
        self.x_col = x_col
        self.y_col = y_col
        self.val_col = val_col

    def build(self):
        if not validate_chart_data(self.df, [self.x_col, self.y_col, self.val_col]):
            return create_empty_chart()

        # Pivot data for heatmap if not already pivoted (simple mock logic)
        pivot_df = self.df.pivot(index=self.y_col, columns=self.x_col, values=self.val_col)
        
        self.fig = px.imshow(
            pivot_df,
            color_continuous_scale=[self.secondary_color, self.primary_color],
            aspect="auto"
        )
        self._apply_theme()
        return self.fig
