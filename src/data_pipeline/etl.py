import pandas as pd
import time
import logging
from pathlib import Path
import sys

# Add root to sys.path to allow relative imports if run as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.logger import get_logger
from src.validation.contracts import raw_contract, gold_contract
from src.validation.reports import generate_dataset_version, generate_data_quality_report, generate_pipeline_summary
from src.data_pipeline.cleaning import clean_data
from src.data_pipeline.feature_engineering import engineer_features
from src.data_pipeline.export import export_bronze, export_silver, export_gold

logger = get_logger(__name__)

def run_etl():
    start_time = time.time()
    metrics = {}
    
    logger.info("Starting Netflix ETL Pipeline")
    
    # --- STAGE 0: RAW ---
    raw_path = Path("data/raw/netflix_titles.csv")
    if not raw_path.exists():
        logger.error(f"Raw data not found at {raw_path}")
        raise FileNotFoundError(f"Raw data missing: {raw_path}")
        
    df_raw = pd.read_csv(raw_path)
    metrics['raw'] = {'records': len(df_raw)}
    
    # Validate Raw
    raw_contract.validate(df_raw)
    export_bronze(df_raw)
    
    # --- STAGE 1: SILVER (Cleaned) ---
    t0 = time.time()
    df_silver = clean_data(df_raw)
    metrics['silver'] = {'duration_sec': round(time.time() - t0, 3)}
    export_silver(df_silver)
    generate_data_quality_report(df_silver, stage="Silver")
    
    # --- STAGE 2: GOLD (Engineered) ---
    t0 = time.time()
    df_gold = engineer_features(df_silver)
    metrics['gold'] = {'duration_sec': round(time.time() - t0, 3)}
    
    # Validate Gold
    gold_contract.validate(df_gold)
    export_gold(df_gold)
    
    # Generate Metadata & Reports
    generate_dataset_version(df_gold, stage="Gold")
    generate_data_quality_report(df_gold, stage="Gold")
    
    generate_pipeline_summary(start_time, time.time(), metrics)
    logger.info("ETL Pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()
