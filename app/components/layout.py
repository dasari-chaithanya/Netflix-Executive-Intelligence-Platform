import streamlit as st

def section_header(title: str, subtitle: str = None):
    """
    Renders a standardized section header.
    
    Purpose: Ensures consistent typography and spacing for major content blocks.
    Props:
        title (str): The main header text (H2).
        subtitle (str, optional): A descriptive sub-header styled as secondary text.
    """
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<p class='text-secondary'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 1.5rem;'/>", unsafe_allow_html=True)

def grid_row(columns_ratios: list):
    """
    Wrapper around st.columns for standard grids.
    
    Purpose: Provides a predictable layout system matching the 12-column grid concept.
    Props:
        columns_ratios (list): Ratios of columns, e.g., [1, 1, 1, 1] for 4 equal cols.
    Usage:
        c1, c2 = grid_row([1, 1])
    Performance Notes: Uses native Streamlit columns. Do not nest excessively.
    """
    return st.columns(columns_ratios)

def chart_container(title: str, help_text: str = None):
    """
    Helper to wrap a chart with a standard title and tooltip.
    
    Purpose: Enforce consistent chart headers before calling Plotly wrappers.
    Props:
        title (str): Chart title.
        help_text (str, optional): Markdown tooltip for additional context.
    """
    if help_text:
        st.markdown(f"**{title}** ℹ️", help=help_text)
    else:
        st.markdown(f"**{title}**")
