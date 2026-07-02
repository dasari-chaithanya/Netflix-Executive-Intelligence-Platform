import plotly.express as px
from app.charts.base import BaseChartBuilder
from app.charts.utils import validate_chart_data, create_empty_chart

class TreemapBuilder(BaseChartBuilder):
    def __init__(self, df, path_cols: list, val_col: str, title: str = None):
        super().__init__(df, title)
        self.path_cols = path_cols
        self.val_col = val_col

    def build(self):
        if not validate_chart_data(self.df, self.path_cols + [self.val_col]):
            return create_empty_chart()
        self.fig = px.treemap(self.df, path=self.path_cols, values=self.val_col, color_discrete_sequence=[self.primary_color, self.secondary_color])
        self._apply_theme()
        return self.fig

class SunburstBuilder(BaseChartBuilder):
    def __init__(self, df, path_cols: list, val_col: str, title: str = None):
        super().__init__(df, title)
        self.path_cols = path_cols
        self.val_col = val_col

    def build(self):
        if not validate_chart_data(self.df, self.path_cols + [self.val_col]):
            return create_empty_chart()
        self.fig = px.sunburst(self.df, path=self.path_cols, values=self.val_col, color_discrete_sequence=[self.primary_color, self.secondary_color])
        self._apply_theme()
        return self.fig

class ScatterBuilder(BaseChartBuilder):
    def __init__(self, df, x_col: str, y_col: str, color_col: str = None, title: str = None):
        super().__init__(df, title)
        self.x_col = x_col
        self.y_col = y_col
        self.color_col = color_col

    def build(self):
        req = [self.x_col, self.y_col]
        if self.color_col: req.append(self.color_col)
        if not validate_chart_data(self.df, req):
            return create_empty_chart()
        self.fig = px.scatter(self.df, x=self.x_col, y=self.y_col, color=self.color_col, color_discrete_sequence=[self.primary_color, self.secondary_color])
        self._apply_theme()
        return self.fig

class BubbleBuilder(ScatterBuilder):
    def __init__(self, df, x_col: str, y_col: str, size_col: str, color_col: str = None, title: str = None):
        super().__init__(df, x_col, y_col, color_col, title)
        self.size_col = size_col

    def build(self):
        req = [self.x_col, self.y_col, self.size_col]
        if self.color_col: req.append(self.color_col)
        if not validate_chart_data(self.df, req):
            return create_empty_chart()
        self.fig = px.scatter(self.df, x=self.x_col, y=self.y_col, size=self.size_col, color=self.color_col, color_discrete_sequence=[self.primary_color, self.secondary_color])
        self._apply_theme()
        return self.fig

class TimelineBuilder(BaseChartBuilder):
    def __init__(self, df, x_start: str, x_end: str, y_col: str, color_col: str = None, title: str = None):
        super().__init__(df, title)
        self.x_start = x_start
        self.x_end = x_end
        self.y_col = y_col
        self.color_col = color_col

    def build(self):
        req = [self.x_start, self.x_end, self.y_col]
        if self.color_col: req.append(self.color_col)
        if not validate_chart_data(self.df, req):
            return create_empty_chart()
        self.fig = px.timeline(self.df, x_start=self.x_start, x_end=self.x_end, y=self.y_col, color=self.color_col, color_discrete_sequence=[self.primary_color, self.secondary_color])
        self._apply_theme()
        return self.fig
