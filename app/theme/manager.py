import streamlit as st
from app.theme.provider import theme_provider
from app.theme.generator import generate_css
from app.state.store import get_theme, get_density

def inject_custom_css():
    """Generates and injects CSS based on active theme and design tokens."""
    tokens = theme_provider.get_tokens()
    current_theme = get_theme()
    current_density = get_density()
    brand_primary = theme_provider.get_color("brand", "red")
    
    css = generate_css(tokens, current_theme, current_density)
    st.markdown(css, unsafe_allow_html=True)
