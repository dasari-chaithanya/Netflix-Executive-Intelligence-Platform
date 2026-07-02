import pandas as pd

def get_growth_velocity(df: pd.DataFrame, reference_year: int = None) -> float:
    """
    Calculates Growth Velocity (YoY %).
    Formula: Percentage change in titles added vs previous year.
    """
    if 'year_added' not in df.columns:
        raise ValueError("DataFrame must contain 'year_added' column.")
        
    if reference_year is None:
        reference_year = int(df['year_added'].max())
        
    current_year_count = len(df[df['year_added'] == reference_year])
    prev_year_count = len(df[df['year_added'] == (reference_year - 1)])
    
    if prev_year_count == 0:
        return 0.0 # Avoid division by zero, assuming 0 baseline means no prior data
        
    return ((current_year_count - prev_year_count) / prev_year_count) * 100
