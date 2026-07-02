import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent) if 'pages' not in __file__ else str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from app.viewmodels.geography import GeographyViewModel
from app.components.cards import story_card
import plotly.express as px

st.markdown("<h1>Market Expansion</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'><strong>Business Question:</strong> Where should Netflix allocate its next $100M regional production budget?</div>", unsafe_allow_html=True)

viewmodel = GeographyViewModel()
data = viewmodel.get_data()

portfolio_mode = st.session_state.get("portfolio_mode", False)

if not data["valid"]:
    st.warning("No titles match the current filter criteria.")
    if st.button("Reset Filters"):
        st.session_state.filters = {}
        st.rerun()
    st.stop()

# Choropleth Map
countries, counts = zip(*data["top_countries"].items())
map_fig = px.choropleth(
    locations=countries,
    locationmode="country names",
    color=counts,
    color_continuous_scale=["#141414", "#E50914"]
)
map_fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular', bgcolor='rgba(0,0,0,0)'),
    margin=dict(t=0, l=0, r=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False
)

story_card(
    title="Production Hotspots",
    value="United States",
    delta="Leader",
    trend="flat",
    period="Current Filters",
    chart_fig=map_fig,
    summary="The US and India remain the primary drivers of content production.",
    recommendation="Consider increasing investments in emerging markets (e.g., South Korea, Spain) to capture localized growth.",
    explanation={"why": "Local content drives local subscriber growth.", "impact": "Heavy US bias limits international penetration.", "opportunity": "High ROI in APAC."} if portfolio_mode else None
)
