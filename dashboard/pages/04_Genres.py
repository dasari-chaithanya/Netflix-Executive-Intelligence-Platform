import streamlit as st
import pandas as pd
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.visualization import plot_top_genres_bar, plot_genre_treemap, plot_genre_sunburst, plot_genre_heatmap

st.set_page_config(page_title="Genres - Netflix Content Strategy", page_icon="🎭", layout="wide")
st.title("🎭 04: Genre Analysis")

if 'filtered_df' not in st.session_state:
    st.warning("Please start from `streamlit_app.py`.")
    st.stop()

df = st.session_state['filtered_df']
if len(df) == 0:
    st.error("No data available for the selected filters.")
    st.stop()

st.markdown("### Top Genres")
fig1 = plot_top_genres_bar(df, save=False)
if fig1: st.pyplot(fig1, use_container_width=True)

st.markdown("### Genre Heatmap by Year")
fig2 = plot_genre_heatmap(df, save=False)
if fig2: st.pyplot(fig2, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("### Genre Sunburst")
    fig3 = plot_genre_sunburst(df, save=False)
    if fig3: st.plotly_chart(fig3, use_container_width=True)

with c2:
    st.markdown("### Genre Treemap")
    fig4 = plot_genre_treemap(df, save=False)
    if fig4: st.plotly_chart(fig4, use_container_width=True)
