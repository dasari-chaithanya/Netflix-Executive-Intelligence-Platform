"""
Centralized business thresholds and logic rules.
No UI page should hardcode threshold checking.
"""

# Thresholds for KPIs
THRESHOLDS = {
    "catalog_freshness": {
        "good_min": 35.0, # Target is > 35% of catalog added in last 24mo
        "warning_min": 25.0
    },
    "average_age": {
        "good_max": 4.5, # Target is < 4.5 years old on average
        "warning_max": 6.0
    },
    "survival_rate": {
        "good_min": 30.0,
        "warning_min": 20.0
    },
    "mature_share": {
        "good_min": 40.0,
        "warning_min": 25.0
    }
}

def evaluate_kpi_trend(metric: str, current_value: float, previous_value: float = None) -> str:
    """Returns 'up', 'down', or 'flat' based on business logic."""
    if previous_value is None:
        return "flat"
    
    if current_value > previous_value:
        return "up"
    elif current_value < previous_value:
        return "down"
    return "flat"

def get_status_color(metric: str, value: float) -> str:
    """Returns 'green', 'orange', 'red' based on threshold mapping."""
    if metric not in THRESHOLDS:
        return "gray"
        
    t = THRESHOLDS[metric]
    
    # If metric is "higher is better"
    if "good_min" in t:
        if value >= t["good_min"]: return "green"
        if value >= t["warning_min"]: return "orange"
        return "red"
        
    # If metric is "lower is better"
    if "good_max" in t:
        if value <= t["good_max"]: return "green"
        if value <= t["warning_max"]: return "orange"
        return "red"
        
    return "gray"
