import streamlit as st
from app.data.loader import load_processed_data
from app.state.store import update_filter, get_filters, reset_filters

def _get_unique_list_items(series):
    """Extracts unique items from a series of strings (e.g. 'Action, Drama')"""
    items = set()
    for row in series.dropna():
        for item in str(row).split(','):
            items.add(item.strip())
    return sorted(list(items))

def global_filter_panel():
    """
    Renders the global sidebar filter controls using actual dataset values.
    """
    st.sidebar.markdown("### Global Filters")
    
    df = load_processed_data()
    if df.empty:
        st.sidebar.warning("No data available.")
        return
        
    current_filters = get_filters()
    
    # Types
    types = ["All"] + sorted(df["type"].dropna().unique().tolist()) if "type" in df.columns else ["All", "Movie", "TV Show"]
    type_idx = types.index(current_filters.get("content_type", "All")) if current_filters.get("content_type", "All") in types else 0
    content_type = st.sidebar.selectbox("Content Type", types, index=type_idx)
    
    # Years
    min_yr = int(df["release_year"].min()) if "release_year" in df.columns else 1920
    max_yr = int(df["release_year"].max()) if "release_year" in df.columns else 2024
    curr_yr = current_filters.get("release_year", (min_yr, max_yr))
    years = st.sidebar.slider("Release Year", min_value=min_yr, max_value=max_yr, value=curr_yr)
    
    # Genres
    all_genres = _get_unique_list_items(df["genres"]) if "genres" in df.columns else []
    genres = st.sidebar.multiselect("Genres", all_genres, default=current_filters.get("genres", []))
    
    # Countries
    all_countries = _get_unique_list_items(df["country"]) if "country" in df.columns else []
    countries = st.sidebar.multiselect("Countries", all_countries, default=current_filters.get("countries", []))
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Apply", type="primary", use_container_width=True):
            update_filter("content_type", content_type)
            update_filter("release_year", years)
            update_filter("genres", genres)
            update_filter("countries", countries)
            st.rerun()
    with col2:
        if st.button("Reset", type="secondary", use_container_width=True):
            reset_filters()
            st.rerun()

def filter_chips():
    """
    Renders active filters as visual chips above the main content.
    
    Purpose: Always visible confirmation to the user of what data they are viewing.
    Accessibility: Needs appropriate aria labels for screen readers when removing chips.
    """
    # Dummy implementation for UI structure
    st.markdown("""
    <div style="display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;">
        <span style="background: #333; padding: 4px 12px; border-radius: 16px; font-size: 0.8rem;">Type: All &times;</span>
        <span style="background: #333; padding: 4px 12px; border-radius: 16px; font-size: 0.8rem;">Years: 2010-2024 &times;</span>
    </div>
    """, unsafe_allow_html=True)
