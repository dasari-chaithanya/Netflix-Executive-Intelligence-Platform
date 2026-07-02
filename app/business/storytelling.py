"""
Narrative generation layer. 
Turns analytics and metrics into executive summaries, insights, and recommendations.
"""
from app.business.rules import get_status_color

def generate_executive_summary(kpis: dict) -> str:
    """Generates a high-level narrative summary from a dictionary of KPI results."""
    if not kpis:
        return "No data available to generate an executive summary."
        
    freshness = kpis.get("catalog_freshness", {}).get("value", 0)
    age = kpis.get("average_content_age", {}).get("value", 0)
    
    status = "healthy" if get_status_color("catalog_freshness", freshness) == "green" else "at risk of stagnation"
    
    return f"""
    The current filtered catalog is **{status}**, with a freshness index of **{freshness:.1f}%**.
    The average content age is **{age:.1f} years**, indicating the balance between legacy library titles and new acquisitions.
    Continue monitoring genre saturation to ensure content acquisition aligns with audience diversity metrics.
    """

def generate_insight(metric_name: str, current_val: float, context: str) -> dict:
    """Generates a structured insight based on metric values."""
    status = get_status_color(metric_name, current_val)
    
    if status == "green":
        title = f"Strong {metric_name.replace('_', ' ').title()}"
        text = f"The current value of {current_val:.1f} indicates strong performance against the benchmark."
    elif status == "orange":
        title = f"Monitor {metric_name.replace('_', ' ').title()}"
        text = f"The current value of {current_val:.1f} is acceptable but approaching warning thresholds."
    else:
        title = f"Critical Risk: {metric_name.replace('_', ' ').title()}"
        text = f"The current value of {current_val:.1f} falls below acceptable business thresholds. Immediate action required."
        
    return {"title": title, "text": f"{text} Context: {context}"}

def generate_recommendation(insight_status: str, domain: str) -> dict:
    """Generates a recommendation based on insight severity."""
    if insight_status == "green":
        return {"title": "Maintain Investment", "action": f"Continue current content acquisition strategy in the {domain} domain."}
    elif insight_status == "orange":
        return {"title": "Optimize Portfolio", "action": f"Review bottom-performing titles in the {domain} domain for potential licensing expiration."}
    else:
        return {"title": "Shift Investment", "action": f"Pause new acquisitions in the {domain} domain and reallocate budget to higher-performing segments."}
