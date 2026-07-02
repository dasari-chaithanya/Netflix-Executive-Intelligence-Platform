import streamlit as st
import pandas as pd
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.visualization import plot_content_type_by_year_area, plot_movie_duration_histogram, plot_duration_boxplot, plot_tv_seasons_bar

st.set_page_config(page_title="Content Dist - Netflix Content Strategy", page_icon="📊", layout="wide")
st.title("📊 02: Content Distribution & Duration")

if 'filtered_df' not in st.session_state:
    st.warning("Please start from `streamlit_app.py`.")
    st.stop()

df = st.session_state['filtered_df']
if len(df) == 0:
    st.error("No data available for the selected filters.")
    st.stop()

st.markdown("### Content Types Over Time")
fig1 = plot_content_type_by_year_area(df, save=False)
if fig1: st.pyplot(fig1, use_container_width=True)

st.markdown("### Movie Duration Analysis")
c1, c2 = st.columns(2)
with c1:
    fig2 = plot_movie_duration_histogram(df, save=False)
    if fig2: st.pyplot(fig2, use_container_width=True)
with c2:
    fig3 = plot_duration_boxplot(df, save=False)
    if fig3: st.pyplot(fig3, use_container_width=True)

st.markdown("### TV Show Season Lengths")
fig4 = plot_tv_seasons_bar(df, save=False)
if fig4: st.pyplot(fig4, use_container_width=True)
