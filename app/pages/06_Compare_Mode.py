import streamlit as st
import random
from app.components.cards import story_card

st.markdown("<h1>Compare Mode: Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'>Side-by-side analysis of key operational markets.</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    market_1 = st.selectbox("Market A", ["United States", "India", "United Kingdom", "South Korea"])
    st.markdown(f"### {market_1} Performance")
    
    val1 = "3,200" if market_1 == "United States" else "980" if market_1 == "India" else "750"
    story_card(
        title="Total Catalog Size",
        value=val1,
        delta="+12%",
        trend="up",
        period="YTD",
        badge="Healthy",
        summary=f"{market_1} maintains strong volume.",
        recommendation={
            "priority": "MEDIUM",
            "impact": "★★★☆☆",
            "confidence": "85%",
            "reach": "Regional",
            "action": f"Maintain localized production pipelines in {market_1}."
        }
    )

with col2:
    market_2 = st.selectbox("Market B", ["India", "United States", "United Kingdom", "South Korea"])
    st.markdown(f"### {market_2} Performance")
    
    val2 = "3,200" if market_2 == "United States" else "980" if market_2 == "India" else "750"
    story_card(
        title="Total Catalog Size",
        value=val2,
        delta="+24%",
        trend="up",
        period="YTD",
        badge="Growing",
        summary=f"{market_2} shows accelerated acquisition pacing.",
        recommendation={
            "priority": "HIGH",
            "impact": "★★★★☆",
            "confidence": "92%",
            "reach": "Regional",
            "action": f"Double marketing spend in {market_2} to capitalize on rapid catalog expansion."
        }
    )
    
if st.button("Continue to Growth Intelligence ➔"):
    st.switch_page("app/pages/05_Growth_Intelligence.py")
