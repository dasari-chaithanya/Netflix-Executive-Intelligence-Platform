import pandas as pd
import streamlit as st
import logging

logger = logging.getLogger(__name__)

@st.cache_data(show_spinner=False)
def load_processed_data() -> pd.DataFrame:
    """
    Loads the optimized Parquet dataset for the dashboard.
    Cached indefinitely within the session to prevent disk I/O on reruns.
    """
    try:
        df = pd.read_parquet("data/processed/netflix_features.parquet")
        logger.info(f"Loaded Parquet data successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Failed to load Parquet dataset: {e}")
        # Return empty dataframe with expected columns if file is missing
        return pd.DataFrame()
