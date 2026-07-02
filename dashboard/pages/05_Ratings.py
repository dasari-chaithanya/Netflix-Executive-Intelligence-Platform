import streamlit as st
import pandas as pd
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.visualization import plot_rating_distribution_bar, plot_rating_by_type_grouped, plot_rating_pie, plot_rating_heatmap_by_year

st.set_page_config(page_title="Ratings - Netflix Content Strategy", page_icon="🔞", layout="wide")
st.title("🔞 05: Ratings & Audience Targeting")

if 'filtered_df' not in st.session_state:
    st.warning("Please start from `streamlit_app.py`.")
    st.stop()

df = st.session_state['filtered_df']
if len(df) == 0:
    st.error("No data available for the selected filters.")
    st.stop()

st.markdown("### Rating Distribution")
c1, c2 = st.columns(2)
with c1:
    fig1 = plot_rating_distribution_bar(df, save=False)
    if fig1: st.pyplot(fig1, use_container_width=True)
with c2:
    fig2 = plot_rating_pie(df, save=False)
    if fig2: st.pyplot(fig2, use_container_width=True)

st.markdown("### Ratings by Content Type")
fig3 = plot_rating_by_type_grouped(df, save=False)
if fig3: st.pyplot(fig3, use_container_width=True)

st.markdown("### Ratings Over Time")
fig4 = plot_rating_heatmap_by_year(df, save=False)
if fig4: st.pyplot(fig4, use_container_width=True)
