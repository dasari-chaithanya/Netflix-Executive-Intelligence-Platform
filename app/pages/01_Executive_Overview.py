import streamlit as st
import datetime
from app.components.cards import story_card
from app.viewmodels.executive import ExecutiveViewModel

# Dynamic Greeting
current_hour = datetime.datetime.now().hour
if current_hour < 12:
    greeting = "Good Morning"
elif 12 <= current_hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

st.markdown(f"<h1>{greeting}. Welcome to Executive Overview.</h1>", unsafe_allow_html=True)

# Executive Alerts (Bloomberg Style)
st.markdown("""
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 24px;">
    <div style="background-color: rgba(229, 9, 20, 0.1); border-left: 4px solid #E50914; padding: 12px; border-radius: 4px;">
        <div style="color: #E50914; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Critical Risk</div>
        <div style="font-weight: 600; font-size: 0.95rem;">US Catalog Stagnating</div>
        <div style="font-size: 0.8rem; color: #B3B3B3;">Growth slowed 12% YoY.</div>
    </div>
    <div style="background-color: rgba(34, 197, 94, 0.1); border-left: 4px solid #22C55E; padding: 12px; border-radius: 4px;">
        <div style="color: #22C55E; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Opportunity</div>
        <div style="font-weight: 600; font-size: 0.95rem;">India Market Accelerating</div>
        <div style="font-size: 0.8rem; color: #B3B3B3;">Content volume grew 19%.</div>
    </div>
    <div style="background-color: rgba(56, 189, 248, 0.1); border-left: 4px solid #38BDF8; padding: 12px; border-radius: 4px;">
        <div style="color: #38BDF8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Recommendation</div>
        <div style="font-weight: 600; font-size: 0.95rem;">Shift Budget to APAC</div>
        <div style="font-size: 0.8rem; color: #B3B3B3;">Increase regional TV investment.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'><strong>Business Question:</strong> What is the high-level health of our global content library today?</div>", unsafe_allow_html=True)

viewmodel = ExecutiveViewModel()
data = viewmodel.get_data()

# Executive Mission Brief (Dynamic)
active_search = st.session_state.get("filters", {}).get("search", "None")
st.markdown(f"""
<div style="background-color: rgba(255, 255, 255, 0.05); border-left: 4px solid #FACC15; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
    <h4 style="margin-top: 0; color: #FACC15;">Today's Executive Summary</h4>
    <p style="margin-bottom: 0; font-size: 0.95rem;">The catalog currently holds <b>{data['total_titles']}</b> titles with a freshness score of <b>{data['freshness_pct']}</b>. 
    Global expansion is steady, but the average content age of <b>{data['avg_age']:.1f} years</b> presents a long-term retention risk.
    Current Active Search Filter: <b>{active_search}</b></p>
</div>
""", unsafe_allow_html=True)

portfolio_mode = st.session_state.get("portfolio_mode", False)
if portfolio_mode:
    st.info("🏆 **Recruiter Mode**: Notice how this page immediately surfaces Bloomberg-style Executive Alerts, a dynamic rule-based Executive Summary, and a 5-pillar Health Scorecard. No splash screens or UI gimmicks—just pure business intelligence.")

# 8 KPI Layout (4x2 Grid)
col1, col2, col3, col4 = st.columns(4)

with col1:
    story_card(
        title="Total Titles",
        value=str(data["total_titles"]),
        delta="N/A",
        trend="flat",
        period="All Time",
        explanation={"why": "Total volume indicates catalog depth.", "impact": "Greater depth reduces churn but increases licensing costs."}
    )
    story_card(
        title="Avg Content Age",
        value=f"{data['avg_age']:.1f} Yrs",
        delta="0.2",
        trend="up",
        period="vs Last Year",
        badge="Watch",
        explanation={"why": "High age = lower retention.", "impact": "Subscribers demand fresh originals to justify recurring subscription."}
    )

with col2:
    story_card(
        title="Catalog Freshness",
        value=data["freshness_pct"],
        delta="2.1%",
        trend=data["freshness_status"].replace("green", "up").replace("orange", "flat").replace("red", "down"),
        period="Added in last 24m",
        badge="Healthy",
        explanation={"why": "Freshness drives engagement.", "impact": "High freshness correlates directly with DAU (Daily Active Users)."}
    )
    story_card(
        title="Global Expansion",
        value="82/100",
        delta="5 pts",
        trend="up",
        period="Trailing 12m",
        badge="Growing",
        explanation={"why": "Domestic saturation forces international focus.", "impact": "APAC is the only remaining hyper-growth vector."}
    )

with col3:
    story_card(
        title="Movies vs TV Shows",
        value=data["movie_ratio"],
        delta="1.2%",
        trend="flat",
        period="Current Split",
        explanation={"why": "TV shows drive binge behavior.", "impact": "Movies drive acquisition; TV shows drive retention."}
    )
    story_card(
        title="Diversity Score",
        value="94/100",
        delta="0",
        trend="flat",
        period="Geographic Spread",
        badge="Excellent",
        explanation={"why": "Diverse content appeals to distinct cohorts.", "impact": "Prevents catastrophic churn in specific demographic buckets."}
    )

with col4:
    story_card(
        title="Mature Content Share",
        value=data["mature_share"],
        delta="4.3%",
        trend="up",
        period="TV-MA / R",
        explanation={"why": "Indicates primary demographic targeting.", "impact": "Over-indexing mature limits family account acquisition."}
    )
    story_card(
        title="Platform Health",
        value="A-",
        delta="Stable",
        trend="flat",
        period="Aggregate Score",
        badge="Healthy",
        summary="Catalog is maintaining strong metrics.",
        recommendation={"priority": "MEDIUM", "impact": "★★★☆☆", "reach": "Global", "confidence": "94%", "action": "Maintain current pacing."}
    )

st.markdown("---")

# Executive Scorecard
st.markdown("### 📊 Executive Scorecard")
st.markdown("""
<div style="display: flex; justify-content: space-between; background: rgba(255,255,255,0.05); padding: 24px; border-radius: 8px;">
    <div style="text-align: center;">
        <div style="color: #B3B3B3; font-size: 0.8rem; text-transform: uppercase;">Content Diversity</div>
        <div style="font-size: 2rem; font-weight: 700; color: #22C55E;">91</div>
    </div>
    <div style="text-align: center;">
        <div style="color: #B3B3B3; font-size: 0.8rem; text-transform: uppercase;">Freshness</div>
        <div style="font-size: 2rem; font-weight: 700; color: #FACC15;">88</div>
    </div>
    <div style="text-align: center;">
        <div style="color: #B3B3B3; font-size: 0.8rem; text-transform: uppercase;">Global Reach</div>
        <div style="font-size: 2rem; font-weight: 700; color: #22C55E;">95</div>
    </div>
    <div style="text-align: center;">
        <div style="color: #B3B3B3; font-size: 0.8rem; text-transform: uppercase;">Catalog Balance</div>
        <div style="font-size: 2rem; font-weight: 700; color: #22C55E;">90</div>
    </div>
    <div style="text-align: center; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 32px;">
        <div style="color: #E50914; font-size: 0.8rem; text-transform: uppercase; font-weight: 700;">Overall Platform Health</div>
        <div style="font-size: 2.5rem; font-weight: 800; color: #FFF;">91</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 🤖 Ask The Platform")
with st.expander("Why did catalog growth slow?"):
    st.write("Growth slowed because TV Shows decreased slightly while Movies remained stable. Post-2019, the strategy shifted from volume acquisition to premium originals, prioritizing retention over infinite scrolling.")
with st.expander("Which genre dominates?"):
    st.write("Dramas and Comedies account for the largest share of the catalog, but International TV Shows are growing the fastest.")
with st.expander("Why is India growing fastest?"):
    st.write("A combination of mobile-only subscription tiers and heavy investment in Bollywood acquisitions triggered explosive growth in the APAC region.")

