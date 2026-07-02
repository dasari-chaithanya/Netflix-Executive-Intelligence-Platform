import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent) if 'pages' not in __file__ else str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st

st.markdown("<h1>Business Glossary</h1>", unsafe_allow_html=True)
st.markdown("<div class='text-secondary' style='margin-bottom: 24px;'>Standardized definitions and business rules for catalog metrics.</div>", unsafe_allow_html=True)

metrics = [
    {
        "Metric": "Catalog Freshness",
        "Formula": "(Titles added in last 24 months) / (Total Titles)",
        "Interpretation": "Measures the recency of the available catalog.",
        "Impact": "High freshness correlates with lower subscriber churn and higher DAU (Daily Active Users)."
    },
    {
        "Metric": "Average Content Age",
        "Formula": "Mean(Current Year - release_year)",
        "Interpretation": "The average age of the intellectual property.",
        "Impact": "An aging catalog requires aggressive acquisition to maintain perceived value."
    },
    {
        "Metric": "Movie to TV Ratio",
        "Formula": "(Total Movies) / (Total TV Shows)",
        "Interpretation": "The structural balance of the platform.",
        "Impact": "Movies drive top-of-funnel acquisition (marketing hooks), while TV shows drive bottom-of-funnel retention (binge watching)."
    },
    {
        "Metric": "Global Expansion Score",
        "Formula": "Weighted index of (Non-US Production Volume) + (Non-US YoY Growth Rate)",
        "Interpretation": "Measures platform reliance on domestic (US) pipelines.",
        "Impact": "A higher score indicates better risk distribution against regional strikes or licensing disputes."
    }
]

for m in metrics:
    st.markdown(f"### {m['Metric']}")
    st.markdown(f"**Formula:** `{m['Formula']}`")
    st.markdown(f"**Business Interpretation:** {m['Interpretation']}")
    st.markdown(f"**Decision Impact:** {m['Impact']}")
    st.markdown("---")
