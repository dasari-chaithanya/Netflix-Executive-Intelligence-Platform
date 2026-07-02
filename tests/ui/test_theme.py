import pytest
from app.theme.provider import ThemeProvider

def test_theme_provider_loads_tokens():
    provider = ThemeProvider()
    tokens = provider.get_tokens()
    
    assert "color" in tokens
    assert "brand" in tokens["color"]
    assert "red" in tokens["color"]["brand"]

def test_theme_provider_get_color():
    provider = ThemeProvider()
    
    # We expect it to pull the actual JSON file during testing if run from root
    color = provider.get_color("brand", "red")
    assert color.startswith("#")

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(r, g, b):
    # sRGB luminance
    a = [v / 255 for v in (r, g, b)]
    a = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in a]
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def calculate_contrast_ratio(hex1, hex2):
    l1 = get_luminance(*hex_to_rgb(hex1))
    l2 = get_luminance(*hex_to_rgb(hex2))
    
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def test_theme_contrast_ratio_wcag():
    provider = ThemeProvider()
    tokens = provider.get_tokens()
    
    # Mock fallback if tokens aren't fully loaded
    bg_dark = tokens.get("color", {}).get("background", {}).get("app", "#141414")
    text_light = tokens.get("color", {}).get("text", {}).get("primary", "#FFFFFF")
    
    contrast = calculate_contrast_ratio(bg_dark, text_light)
    
    # WCAG AA requires 4.5:1 for normal text
    assert contrast >= 4.5, f"Contrast ratio {contrast:.2f} fails WCAG AA standard."
