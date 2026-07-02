import plotly.express as px
from app.charts.base import BaseChartBuilder
from app.charts.utils import validate_chart_data, create_empty_chart

class MapChartBuilder(BaseChartBuilder):
    def __init__(self, df, loc_col: str, val_col: str, title: str = None):
        super().__init__(df, title)
        self.loc_col = loc_col
        self.val_col = val_col

    def build(self):
        if not validate_chart_data(self.df, [self.loc_col, self.val_col]):
            return create_empty_chart()

        self.fig = px.choropleth(
            self.df,
            locations=self.loc_col,
            locationmode="ISO-3",
            color=self.val_col,
            color_continuous_scale=[self.secondary_color, self.primary_color]
        )
        self._apply_theme()
        self.fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=True))
        return self.fig
