import streamlit as st
import pandas as pd
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.visualization import plot_yearly_additions_line, plot_cumulative_growth, plot_weekday_additions

st.set_page_config(page_title="Timeline - Netflix Content Strategy", page_icon="📅", layout="wide")
st.title("📅 02: Timeline & Growth")

if 'filtered_df' not in st.session_state:
    st.warning("Please start from `streamlit_app.py`.")
    st.stop()

df = st.session_state['filtered_df']
if len(df) == 0:
    st.error("No data available for the selected filters.")
    st.stop()

st.markdown("### Historical Growth")
c1, c2 = st.columns(2)

with c1:
    fig1 = plot_yearly_additions_line(df, save=False)
    if fig1: st.pyplot(fig1, use_container_width=True)

with c2:
    fig2 = plot_cumulative_growth(df, save=False)
    if fig2: st.pyplot(fig2, use_container_width=True)

st.markdown("### Addition Patterns")
fig3 = plot_weekday_additions(df, save=False)
if fig3: st.pyplot(fig3, use_container_width=True)
