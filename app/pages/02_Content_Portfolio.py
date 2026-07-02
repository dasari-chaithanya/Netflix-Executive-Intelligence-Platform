import streamlit as st
import plotly.express as px
from app.viewmodels.content import ContentViewModel
from app.components.cards import story_card

st.markdown("<h1>Content Portfolio</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'><strong>Business Question:</strong> What is the structural composition and rating focus of our global catalog?</div>", unsafe_allow_html=True)

viewmodel = ContentViewModel()
data = viewmodel.get_data()

portfolio_mode = st.session_state.get("portfolio_mode", False)

if not data["valid"]:
    st.warning("No titles match the current filter criteria.")
    if st.button("Reset Filters"):
        st.session_state.filters = {}
        st.rerun()
    st.stop()

# Generate a Treemap for Ratings
treemap_fig = px.treemap(
    names=list(data["rating_distribution"].keys()),
    parents=["Catalog"] * len(data["rating_distribution"]),
    values=list(data["rating_distribution"].values()),
    color_discrete_sequence=["#E50914", "#A855F7", "#38BDF8", "#FACC15"]
)
treemap_fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor="rgba(0,0,0,0)")

story_card(
    title="Primary Rating Focus",
    value="TV-MA",
    delta="Dominant",
    trend="flat",
    period="All Time",
    chart_fig=treemap_fig,
    summary="The catalog leans heavily mature, with TV-MA and R ratings dominating the treemap.",
    recommendation="Maintain focus on mature audiences, but ensure Kids/Family content is refreshed before holiday seasons.",
    explanation={"why": "Ratings determine target demographics.", "impact": "Over-indexing mature limits family acquisition."} if portfolio_mode else None
)
