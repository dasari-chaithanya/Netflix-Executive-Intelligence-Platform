import streamlit as st
import pandas as pd
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.visualization import plot_content_type_donut, plot_decade_distribution, plot_top_ratings_bar

st.set_page_config(page_title="Overview - Netflix Content Strategy", page_icon="📈", layout="wide")
st.title("📈 01: Overview & Content Distribution")

if 'filtered_df' not in st.session_state:
    st.warning("Please start from `streamlit_app.py`.")
    st.stop()

df = st.session_state['filtered_df']

if len(df) == 0:
    st.error("No data available for the selected filters.")
    st.stop()

st.markdown("### Content Balance")
c1, c2 = st.columns(2)

with c1:
    fig1 = plot_content_type_donut(df, save=False)
    st.pyplot(fig1, use_container_width=True)

with c2:
    fig2 = plot_decade_distribution(df, save=False)
    st.pyplot(fig2, use_container_width=True)

st.markdown("### Content Ratings")
fig3 = plot_top_ratings_bar(df, save=False)
st.pyplot(fig3, use_container_width=True)
