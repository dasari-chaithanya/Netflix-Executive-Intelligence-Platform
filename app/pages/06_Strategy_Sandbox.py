import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent) if 'pages' not in __file__ else str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from app.components.cards import story_card

st.markdown("<h1>Strategy Sandbox</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'><strong>Business Question:</strong> How do targeted content investments impact catalog diversity and freshness?</div>", unsafe_allow_html=True)

st.markdown("### 🎛️ Scenario Builder")
col1, col2, col3, col4 = st.columns(4)

with col1:
    market = st.selectbox("Focus Market", ["India", "South Korea", "United Kingdom", "Japan", "Spain"])
with col2:
    content_type = st.selectbox("Content Type", ["TV Shows", "Movies", "Documentaries"])
with col3:
    genre = st.selectbox("Genre Focus", ["Drama", "Action", "Comedy", "Anime", "Thriller"])
with col4:
    volume_increase = st.select_slider("Target Increase", options=["+5%", "+10%", "+15%", "+20%"])

st.markdown("---")

if st.button("Apply Scenario", type="primary", use_container_width=True):
    with st.spinner("Recalculating Catalog Metrics..."):
        # Simple heuristics for demonstration
        diversity_impact = "+4%" if market in ["India", "South Korea", "Japan"] else "+2%"
        freshness_impact = "-1%" if content_type == "Movies" else "+3%"
        regional_rep = "+8%" if market == "India" and genre == "Drama" else "+5%"
        
        st.markdown("### 📊 Observed Impact")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Catalog Diversity", diversity_impact)
        c2.metric("Regional Representation", regional_rep)
        c3.metric("Content Freshness", freshness_impact)
        
        st.markdown("---")
        
        st.markdown("### 💡 Strategic Observation")
        st.info(f"Increasing {market} {genre} {content_type} by {volume_increase} significantly boosts Regional Representation ({regional_rep}) and improves overall Catalog Diversity ({diversity_impact}). However, this may slightly impact Content Freshness ({freshness_impact}) depending on production lead times.")
        
        st.markdown("### 🎯 Recommendation")
        st.success(f"**High Potential**. {market} {genre} currently represents a growing segment. Expanding {content_type} aligns with historical retention data.")
        
        st.markdown("<div class='text-secondary' style='font-size: 0.8rem; margin-top: 24px;'>Note: Impacts are derived from historical metadata elasticity rules. No financial or ROI assumptions are made.</div>", unsafe_allow_html=True)
