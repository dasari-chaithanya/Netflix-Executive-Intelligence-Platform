import pandas as pd

def apply_global_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Applies the active global filters to the master DataFrame.
    
    Args:
        df: The raw DataFrame from the loader.
        filters: The dictionary from st.session_state.filters.
    
    Returns:
        Filtered DataFrame.
    """
    if df is None or df.empty:
        return df
        
    filtered = df.copy()

    # Content Type Filter
    content_type = filters.get("content_type", "All")
    if content_type != "All":
        if "type" in filtered.columns:
            filtered = filtered[filtered["type"] == content_type]

    # Release Year Filter
    years = filters.get("release_year", (1920, 2024))
    if "release_year" in filtered.columns:
        filtered = filtered[(filtered["release_year"] >= years[0]) & (filtered["release_year"] <= years[1])]

    # Genres Filter
    genres = filters.get("genres", [])
    if genres and "genres" in filtered.columns:
        # Assuming genres column is a list or comma-separated string based on feature engineering
        # If it's a list, we check for intersection. If string, we use str.contains
        # For robustness with string:
        mask = filtered["genres"].apply(lambda g: any(genre in str(g) for genre in genres))
        filtered = filtered[mask]

    # Countries Filter
    countries = filters.get("countries", [])
    if countries and "country" in filtered.columns:
        mask = filtered["country"].apply(lambda c: any(country in str(c) for country in countries))
        filtered = filtered[mask]

    return filtered
