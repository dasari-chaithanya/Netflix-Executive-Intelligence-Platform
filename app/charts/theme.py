from app.theme.provider import theme_provider
from app.state.store import get_theme

def get_chart_theme_layout() -> dict:
    """Returns a Plotly layout dictionary with the active theme applied."""
    tokens = theme_provider.get_tokens()
    current_theme = get_theme()
    
    # Base layout
    layout = {
        "font": {
            "family": tokens.get("typography", {}).get("fontFamily", {}).get("base", "Inter, sans-serif"),
            "color": tokens.get("color", {}).get("text", {}).get("primary", "#FFF" if current_theme == "dark" else "#000")
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {"l": 10, "r": 10, "t": 30, "b": 10},
        "hoverlabel": {
            "bgcolor": "rgba(20,20,20,0.8)",
            "bordercolor": "rgba(255,255,255,0.1)",
            "font": {"family": "Inter", "color": "#FFF"},
            "align": "left",
            "namelength": -1
        },
        "transition": {"duration": 500, "easing": "cubic-in-out"},
        "xaxis": {
            "showgrid": False,
            "zeroline": False,
            "showline": True,
            "linecolor": tokens.get("color", {}).get("border", {}).get("subtle_dark", "rgba(255,255,255,0.05)"),
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": "rgba(255,255,255,0.08)", # 0.08 opacity as requested
            "zeroline": False,
        }
    }
    return layout
