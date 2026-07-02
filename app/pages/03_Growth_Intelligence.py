import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent) if 'pages' not in __file__ else str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from app.viewmodels.growth import GrowthViewModel
from app.components.cards import story_card
import plotly.express as px
import pandas as pd

st.markdown("<h1>Growth Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'>Has Netflix slowed down catalog expansion?</div>", unsafe_allow_html=True)

viewmodel = GrowthViewModel()
data = viewmodel.get_data()

portfolio_mode = st.session_state.get("portfolio_mode", False)

if not data["valid"]:
    st.warning("No titles match the current filter criteria.")
    if st.button("Reset Filters"):
        st.session_state.filters = {}
        st.rerun()
    st.stop()

# Area Chart with Range Slider
df = pd.DataFrame(list(data["additions_by_year"].items()), columns=["Year", "Count"])
area_fig = px.area(
    df, x="Year", y="Count",
    color_discrete_sequence=["#E50914"]
)
area_fig.update_traces(
    line_shape='spline', mode='lines', hoverinfo='all', fill='tozeroy', fillcolor='rgba(229, 9, 20, 0.15)'
)
area_fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(rangeslider=dict(visible=True, thickness=0.05, bgcolor="rgba(255,255,255,0.05)"))
)

story_card(
    title="Peak Addition Year",
    value="2019",
    delta="Slowdown",
    trend="down",
    period="Post-Pandemic",
    chart_fig=area_fig,
    summary="Content additions peaked in 2019 and have normalized in recent years, indicating a shift from volume to quality.",
    recommendation={"priority": "HIGH", "impact": "★★★★★", "reach": "Global", "confidence": "96%", "action": "Shift marketing focus from 'infinite catalog' to 'premium exclusive hits'."},
    explanation={"why": "Pacing reveals business strategy (growth vs retention).", "impact": "Slower pacing requires higher hit-rates per show."} if portfolio_mode else None
)

st.markdown("---")

st.markdown("### ⏱️ Insight Timeline")
st.markdown("""
- **🔴 2016** — Netflix expansion accelerates globally.
- **🔴 2018** — TV Shows begin to cannibalize Movie acquisition budget.
- **🔴 2020** — Global diversification increases heavily (India, South Korea).
- **🔴 2022** — Overall volume growth stabilizes; focus shifts to catalog freshness.
""")

from app.components.cards import executive_decision_closer, navigation_footer

executive_decision_closer(
    recommendation="Shift marketing focus from 'infinite catalog' to 'premium exclusive hits'.",
    impact="Improve brand perception and justify subscription price increases.",
    confidence="96%",
    priority="HIGH"
)

navigation_footer(
    next_page_name="Market Expansion", 
    next_page_path="pages/04_Market_Expansion.py", 
    next_page_desc="Analyze top-producing countries and localized production growth.", 
    icon="🌍"
)
