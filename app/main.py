import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent) if 'pages' not in __file__ else str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Netflix Executive Intelligence Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

from app.theme.manager import inject_custom_css
from app.components.filters import global_filter_panel
from app.state.store import init_state, get_theme, set_theme, get_density, set_density

# Initialize state and inject CSS
init_state()
inject_custom_css()

# Hide default sidebar nav
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color: #E50914;'>NETFLIX</h1>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 24px; color: #B3B3B3; text-transform: uppercase;'>Executive Intelligence Platform</div>", unsafe_allow_html=True)

    # Recruiter Mode Toggle (Promoted to top, as requested)
    recruiter_mode = st.session_state.get("portfolio_mode", False)
    if st.toggle("🏆 Recruiter Mode", value=recruiter_mode, help="Auto-expands insights and shows architecture details for portfolio review."):
        st.session_state.portfolio_mode = True
    else:
        st.session_state.portfolio_mode = False

    st.markdown("---")

    # Global Search
    search_query = st.text_input("🔍 Search Platform...", placeholder="e.g. India, Drama, TV-MA")
    if search_query:
        st.session_state.filters["search"] = search_query
    elif "search" in st.session_state.filters:
        del st.session_state.filters["search"]
        
    st.markdown("---")
    
    # Premium Navigation
    st.markdown("### 🏠 Platform")
    if st.button("Executive Overview", use_container_width=True):
        st.switch_page("app/pages/01_Executive_Overview.py")
        
    st.markdown("### 📊 Intelligence")
    if st.button("Growth Intelligence", use_container_width=True):
        st.switch_page("app/pages/03_Growth_Intelligence.py")
    if st.button("Market Expansion", use_container_width=True):
        st.switch_page("app/pages/04_Market_Expansion.py")
    if st.button("Content Portfolio", use_container_width=True):
        st.switch_page("app/pages/02_Content_Portfolio.py")
    if st.button("Audience Strategy", use_container_width=True):
        st.switch_page("app/pages/05_Audience_Strategy.py")
        
    st.markdown("### 💡 Strategy")
    if st.button("Compare Markets", use_container_width=True):
        st.switch_page("app/pages/06_Compare_Mode.py")
    if st.button("Strategy Sandbox", use_container_width=True):
        st.switch_page("app/pages/06_Strategy_Sandbox.py")
    if st.button("Recommendations", use_container_width=True):
        st.switch_page("app/pages/07_Insights_Recommendations.py")
        
    st.markdown("---")
    st.markdown("### 📚 Resources")
    if st.button("Business Glossary", use_container_width=True):
        st.switch_page("app/pages/08_Business_Glossary.py")
        
    st.markdown("---")
    
    # Export Report Button
    if st.button("📄 Generate Executive Report", use_container_width=True):
        st.toast("Generating PDF Report... (Simulated)", icon="✅")
    
    st.markdown("---")
    
    # Render data filters
    global_filter_panel()

# Default routing to landing page
st.switch_page("app/pages/01_Executive_Overview.py")
