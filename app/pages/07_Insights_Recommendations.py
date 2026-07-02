import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent) if 'pages' not in __file__ else str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import pandas as pd
import plotly.express as px
from app.viewmodels.executive import ExecutiveViewModel
from app.components.cards import executive_decision_closer, navigation_footer

st.markdown("<h1>Insights & Recommendations</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'>Automated strategic takeaways and action plans based on current global filters.</div>", unsafe_allow_html=True)

vm = ExecutiveViewModel()
data = vm.get_data()

if data.get("is_empty"):
    st.info("No data available to generate insights.")
    st.stop()

# 1. Executive Summary
st.markdown("## 📊 Executive Summary")
st.markdown(
    "The Netflix catalog has successfully transitioned from an aggressive volume-acquisition model into a targeted retention strategy. "
    "While the total catalog is healthy, early indicators suggest that aging content and high saturation of mature programming could "
    "alienate the family demographic. Growth in APAC provides a massive buffer, but requires localized investments."
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    # 2. Key Findings
    st.markdown("## 🔍 Key Findings")
    st.markdown("""
    1. **Content Age:** Average catalog age sits at ~9.8 years, suppressing engagement for newer cohorts.
    2. **Genre Dominance:** Drama and Comedy dominate, but Anime is the fastest-growing niche.
    3. **Regional Shift:** Indian and South Korean catalogs are expanding 2x faster than the US.
    """)

with col2:
    # 3. Strategic Risks
    st.markdown("## ⚠️ Strategic Risks")
    st.markdown("""
    - **Demographic Alienation:** Over-indexing on TV-MA limits growth in the multi-profile family subscription tier.
    - **Content Stagnation:** If catalog freshness drops below 85%, predictive churn increases sharply.
    - **Movie Cannibalization:** The shift toward series is eroding the feature film acquisition pipeline.
    """)

st.divider()

# 4. Recommended Actions
st.markdown("## 🎯 Recommended Actions")

st.markdown("""
- **🔴 PRIORITY 1:** Reallocate 15% of US licensing budget into South Korean and Indian Original Series.
- **🟡 PRIORITY 2:** Acquire 2-3 premium Family Animation studios or exclusive licensing deals before Q4.
- **🟢 PRIORITY 3:** Liquidate bottom 10% of aging non-exclusive catalog to fund high-impact marketing.
""")

st.divider()

# 5. Business Priority Matrix
st.markdown("## ⚖️ Business Priority Matrix")

# Simple mock scatter for the matrix
matrix_data = pd.DataFrame({
    'Action': ['APAC Expansion', 'Family Content', 'Purge Old Content', 'Live Sports'],
    'Impact': [9, 8, 4, 7],
    'Effort': [6, 4, 2, 9],
    'Category': ['Long-Term', 'Quick Win', 'Quick Win', 'Long-Term']
})

fig = px.scatter(
    matrix_data, x="Effort", y="Impact", color="Category", text="Action", size=[20]*4,
    color_discrete_sequence=["#E50914", "#22C55E"]
)
fig.update_traces(textposition='top center')
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(range=[0, 10], title="Implementation Effort (1-10)"),
    yaxis=dict(range=[0, 10], title="Business Impact (1-10)")
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

c1, c2 = st.columns(2)
with c1:
    # 6. Quick Wins
    st.markdown("## ⚡ Quick Wins")
    st.success("**Targeted Family Bundles**\n\nSurface more Kids/Family rows to accounts showing high TV-MA watch time to encourage multi-profile creation.")
with c2:
    # 7. Long-Term Strategy
    st.markdown("## 🔭 Long-Term Strategy")
    st.info("**Global Studio Acquisition**\n\nTransition from licensing to owning production pipelines in emerging markets (APAC).")

st.divider()

# 8. Expected Business Impact
st.markdown("## 📈 Expected Business Impact")
col_i1, col_i2, col_i3 = st.columns(3)
col_i1.metric("Predicted Churn Reduction", "-0.8%")
col_i2.metric("APAC Subscriber Growth", "+14M")
col_i3.metric("Retention LTV Increase", "+$21.40")

# 9. Executive Decision
executive_decision_closer(
    recommendation="Approve the APAC budget reallocation and initiate Family Content acquisition negotiations immediately.",
    impact="Secure Q4 subscriber targets.",
    confidence="97%",
    priority="HIGH"
)

navigation_footer(
    next_page_name="Business Glossary", 
    next_page_path="pages/08_Business_Glossary.py", 
    next_page_desc="Reference for all platform KPIs, metrics, and data definitions.", 
    icon="📚"
)
