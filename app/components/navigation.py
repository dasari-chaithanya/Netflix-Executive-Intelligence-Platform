import streamlit as st
from app.state.store import toggle_theme, get_theme

def render_sidebar():
    """
    Renders standard sidebar elements.
    
    Purpose: Provides application context, branding, and global settings.
    Usage: Call early in `main.py` before page execution logic.
    """
    with st.sidebar:
        st.markdown("## Netflix C-Suite")
        st.caption("Content Strategy & Catalog Intelligence")
        st.divider()
        
        # Note: Navigation links are handled by st.navigation in main.py
        
        st.markdown("### Settings")
        theme_label = "Switch to Light Mode" if get_theme() == "dark" else "Switch to Dark Mode"
        if st.button(theme_label, use_container_width=True):
            toggle_theme()

def render_footer():
    """
    Renders standard footer at the bottom of the page.
    
    Purpose: Branding compliance and legal boilerplate.
    Usage: Call at the very end of `main.py`.
    """
    st.markdown("""
    <div style="margin-top: 50px; text-align: center; color: #666; font-size: 0.8rem; border-top: 1px solid #333; padding-top: 16px;">
        Netflix Content Strategy Platform &copy; 2026. Internal Use Only.
    </div>
    """, unsafe_allow_html=True)
