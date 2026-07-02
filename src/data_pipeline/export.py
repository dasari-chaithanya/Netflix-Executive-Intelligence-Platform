import pandas as pd
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def export_bronze(df: pd.DataFrame, output_dir: str = "data/bronze"):
    """Saves the raw immutable copy to bronze."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    df.to_parquet(Path(output_dir) / "netflix_raw.parquet", index=False)
    logger.info("Exported Bronze dataset.")

def export_silver(df: pd.DataFrame, output_dir: str = "data/silver"):
    """Saves the cleaned dataset to silver."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    df.to_parquet(Path(output_dir) / "netflix_cleaned.parquet", index=False)
    df.to_csv(Path(output_dir) / "netflix_cleaned.csv", index=False)
    logger.info("Exported Silver dataset.")

def export_gold(df: pd.DataFrame, output_dir: str = "data/gold"):
    """Saves the fully engineered dataset to gold & processed."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Parquet (Production Streamlit)
    parquet_path = processed_dir / "netflix_features.parquet"
    df.to_parquet(parquet_path, index=False)
    
    # 2. CSV (Debugging/Excel)
    csv_path = processed_dir / "netflix_features.csv"
    df.to_csv(csv_path, index=False)
    
    # Save copy to Gold
    df.to_parquet(Path(output_dir) / "netflix_gold.parquet", index=False)
    
    logger.info("Exported Gold/Processed datasets (Parquet + CSV).")

def export_kpi_cache(kpi_dict: dict, output_dir: str = "data/processed"):
    """Saves top-level KPIs as JSON for instant dashboard loading."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(output_dir) / "netflix_summary.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(kpi_dict, f, indent=4)
        
    logger.info("Exported KPI Summary Cache to JSON.")
