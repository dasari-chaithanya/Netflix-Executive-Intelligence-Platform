import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.config import FEATURES_CSV, BUSINESS_KPIS
from src.utils import compute_kpis

st.set_page_config(
    page_title="Netflix Content Strategy",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🍿 Netflix Content Strategy Analysis")
st.markdown("### End-to-End Data Analytics Case Study")

@st.cache_data
def get_data():
    if not FEATURES_CSV.exists():
        return None
    df = pd.read_csv(FEATURES_CSV)
    # Parse list strings back to lists
    df['genres'] = df['genres'].apply(
        lambda x: [g.strip() for g in str(x).split(',') if g.strip()] if pd.notna(x) else []
    )
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

df = get_data()

if df is None:
    st.warning("⚠️ Feature dataset not found. Please run the Jupyter notebooks first to generate `data/processed/netflix_features.csv`.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Global Filters")

type_filter = st.sidebar.multiselect(
    "Content Type", 
    options=["Movie", "TV Show"], 
    default=["Movie", "TV Show"]
)

min_year = int(df['release_year'].min(skipna=True)) if not df['release_year'].isna().all() else 1925
max_year = int(df['release_year'].max(skipna=True)) if not df['release_year'].isna().all() else 2026
year_filter = st.sidebar.slider(
    "Release Year", 
    min_value=min_year, max_value=max_year, 
    value=(min_year, max_year)
)

ratings = sorted(df['rating'].dropna().unique().tolist())
rating_filter = st.sidebar.multiselect("Rating", options=ratings, default=ratings)

# --- FILTER DATA ---
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'] >= year_filter[0]) & 
    (df['release_year'] <= year_filter[1]) &
    (df['rating'].isin(rating_filter))
]

st.session_state['filtered_df'] = filtered_df
st.session_state['full_df'] = df

# --- EXPORT ---
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Download Filtered CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='netflix_filtered.csv',
    mime='text/csv',
)

# --- KPI CARDS ---
st.markdown("#### Portfolio Snapshot")
kpis = compute_kpis(filtered_df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Titles", f"{kpis.get('Total Titles', 0):,}")
c2.metric("Movies", f"{kpis.get('Movies', 0):,}")
c3.metric("TV Shows", f"{kpis.get('TV Shows', 0):,}")
c4.metric("Countries Represented", f"{kpis.get('Country Diversity', 0):,}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Avg Movie Duration", f"{kpis.get('Average Movie Duration (min)', 0)} min" if kpis.get('Average Movie Duration (min)') else "N/A")
c6.metric("Top Producing Country", str(kpis.get('Top Producing Country', 'N/A')))
c7.metric("Top Genre", str(kpis.get('Top Genre', 'N/A')))
c8.metric("Median Movie Age", f"{kpis.get('Median Movie Age (years)', 0)} yrs" if kpis.get('Median Movie Age (years)') else "N/A")

st.markdown("---")
st.info("👈 Navigate through the pages in the sidebar to explore deeper insights.")
