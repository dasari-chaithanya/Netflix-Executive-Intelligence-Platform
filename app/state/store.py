import streamlit as st
import json

def init_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark" # Can be 'dark', 'dark+', 'light'
    if "density" not in st.session_state:
        st.session_state.density = "comfortable" # Can be 'compact', 'comfortable', 'presentation'
    if "portfolio_mode" not in st.session_state:
        st.session_state.portfolio_mode = False
    if "filters" not in st.session_state:
        st.session_state.filters = {}

def get_theme():
    return st.session_state.get("theme", "dark")

def set_theme(theme: str):
    st.session_state.theme = theme

def get_density():
    return st.session_state.get("density", "comfortable")

def set_density(density: str):
    st.session_state.density = density
    
def toggle_portfolio_mode():
    st.session_state.portfolio_mode = not st.session_state.get("portfolio_mode", False)

def update_filter(key, value):
    st.session_state.filters[key] = value

def get_filters():
    return st.session_state.get("filters", {})

def reset_filters():
    st.session_state.filters = {}
