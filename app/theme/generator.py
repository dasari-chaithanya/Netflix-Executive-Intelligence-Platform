def generate_css(tokens: dict, current_theme: str, layout_density: str = "comfortable") -> str:
    """Generates the raw CSS string from design tokens, including microinteractions."""
    
    brand_primary = tokens.get("color", {}).get("brand", {}).get("red", "#E50914")
    
    # Theme parsing
    if current_theme == "dark":
        bg_color = tokens.get("color", {}).get("background", {}).get("app_dark", "#000000")
        surface_color = tokens.get("color", {}).get("background", {}).get("surface_dark", "#141414")
        text_primary = tokens.get("color", {}).get("text", {}).get("primary_dark", "#FFFFFF")
        text_secondary = tokens.get("color", {}).get("text", {}).get("secondary_dark", "#B3B3B3")
        border_color = tokens.get("color", {}).get("border", {}).get("subtle_dark", "rgba(255,255,255,0.05)")
    elif current_theme == "dark+":
        bg_color = tokens.get("color", {}).get("background", {}).get("app_dark_plus", "#090909")
        surface_color = tokens.get("color", {}).get("background", {}).get("surface_dark_plus", "#1A1A1A")
        text_primary = tokens.get("color", {}).get("text", {}).get("primary_dark", "#FFFFFF")
        text_secondary = tokens.get("color", {}).get("text", {}).get("secondary_dark", "#B3B3B3")
        border_color = tokens.get("color", {}).get("border", {}).get("subtle_dark", "rgba(255,255,255,0.05)")
    else:
        # Light mode
        bg_color = tokens.get("color", {}).get("background", {}).get("app_light", "#F8F9FA")
        surface_color = tokens.get("color", {}).get("background", {}).get("surface_light", "#FFFFFF")
        text_primary = tokens.get("color", {}).get("text", {}).get("primary_light", "#1A1A1A")
        text_secondary = tokens.get("color", {}).get("text", {}).get("secondary_light", "#666666")
        border_color = tokens.get("color", {}).get("border", {}).get("subtle_light", "rgba(0,0,0,0.05)")

    spacing = tokens.get("spacing", {}).get(layout_density, "16px")
    radius_md = "8px"

    return f"""
    <style>
    /* Reset and Base */
    .stApp {{
        background-color: {bg_color};
        color: {text_primary};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Fade In Animation for elements */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Surface Containers (Cards) */
    .metric-card, .insight-card, .custom-container, .story-card {{
        background-color: {surface_color};
        border-radius: {radius_md};
        padding: {spacing};
        border: 1px solid {border_color};
        margin-bottom: {spacing};
        box-shadow: none; /* No huge shadows */
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        animation: fadeIn 0.4s ease-out forwards;
    }}
    
    /* Card Lift on Hover */
    .story-card:hover, .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: rgba(255,255,255,0.15);
    }}
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6, span, p, div {{
        color: {text_primary};
    }}
    
    .text-secondary {{
        color: {text_secondary} !important;
    }}
    
    .text-positive {{
        color: {tokens.get('color', {{}}).get('status', {{}}).get('positive', '#22C55E')} !important;
    }}
    
    .text-negative {{
        color: {tokens.get('color', {{}}).get('status', {{}}).get('negative', '#EF4444')} !important;
    }}
    
    /* Brand accents */
    .brand-text {{
        color: {brand_primary} !important;
    }}
    
    /* Hide Streamlit Chrome for clean UI */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {surface_color};
        border-right: 1px solid {border_color};
    }}
    
    /* Skeleton Loader */
    .skeleton {{
        animation: skeleton-loading 1s linear infinite alternate;
    }}
    @keyframes skeleton-loading {{
        0% {{ background-color: rgba(255,255,255,0.05); }}
        100% {{ background-color: rgba(255,255,255,0.15); }}
    }}
    </style>
    """
