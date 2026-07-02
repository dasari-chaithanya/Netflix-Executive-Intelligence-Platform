import streamlit as st
import pandas as pd
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.visualization import plot_top_countries_bar, plot_country_treemap, plot_choropleth_map

st.set_page_config(page_title="Countries - Netflix Content Strategy", page_icon="🌍", layout="wide")
st.title("🌍 03: Global Production & Countries")

if 'filtered_df' not in st.session_state:
    st.warning("Please start from `streamlit_app.py`.")
    st.stop()

df = st.session_state['filtered_df']
if len(df) == 0:
    st.error("No data available for the selected filters.")
    st.stop()

st.markdown("### Top Producing Countries")
fig1 = plot_top_countries_bar(df, save=False)
if fig1: st.pyplot(fig1, use_container_width=True)

st.markdown("### Global Map")
fig2 = plot_choropleth_map(df, save=False)
if fig2: st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Country Treemap")
fig3 = plot_country_treemap(df, save=False)
if fig3: st.plotly_chart(fig3, use_container_width=True)
