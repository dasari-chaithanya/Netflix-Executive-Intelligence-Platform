import streamlit as st

def empty_state(message: str = "No data available for the selected filters."):
    """
    Renders a standard empty state message.
    
    Purpose: To handle zero-result queries gracefully without breaking the UI grid.
    Props: message (str)
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🔍</div>
        <div>{message}</div>
    </div>
    """, unsafe_allow_html=True)

def error_component(message: str = "An error occurred while loading this component."):
    """
    Renders a standard error state.
    
    Purpose: To trap exceptions gracefully instead of showing raw Python tracebacks.
    Props: message (str)
    """
    st.error(message, icon="🚨")

def loading_skeleton():
    """
    Renders a pulsing loading skeleton.
    
    Purpose: To provide visual feedback during expensive data loading phases.
    Performance Notes: Uses CSS animation directly to avoid blocking Streamlit thread.
    """
    st.markdown("""
    <div style="animation: pulse 1.5s infinite; background: #333; height: 300px; border-radius: 8px;"></div>
    <style>
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 0.3; }
        100% { opacity: 0.6; }
    }
    </style>
    """, unsafe_allow_html=True)

def info_banner(text: str):
    """Purpose: Show informational toast/banner."""
    st.info(text, icon="ℹ️")

def success_banner(text: str):
    """Purpose: Show success toast/banner."""
    st.success(text, icon="✅")

def warning_banner(text: str):
    """Purpose: Show warning toast/banner."""
    st.warning(text, icon="⚠️")
