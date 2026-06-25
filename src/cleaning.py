"""
cleaning.py
===========
All data cleaning functions for the Netflix Content Strategy Analysis project.
Import these functions in notebooks/02_data_cleaning.ipynb.
"""

from __future__ import annotations

import re
import logging
from typing import Optional

import pandas as pd
import numpy as np

from src.config import RAW_CSV, CLEANED_CSV, CLEANED_PARQUET

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# PIPELINE ENTRY POINT
# ─────────────────────────────────────────────────────────────
def run_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full data cleaning pipeline.

    Steps
    -----
    1. Drop duplicates
    2. Fix column dtypes
    3. Parse date_added → datetime
    4. Parse duration → numeric columns
    5. Normalize country names
    6. Standardize ratings
    7. Fill / flag missing values
    8. Standardize text fields
    9. Split listed_in into genre list

    Parameters
    ----------
    df : pd.DataFrame
        Raw Netflix dataset loaded from netflix_titles.csv.

    Returns
    -------
    pd.DataFrame
        Cleaned dataset ready for feature engineering.
    """
    logger.info("Starting cleaning pipeline …")
    df = df.copy()
    df = drop_duplicates(df)
    df = fix_dtypes(df)
    df = parse_date_added(df)
    df = parse_duration(df)
    df = normalize_countries(df)
    df = standardize_ratings(df)
    df = handle_missing_values(df)
    df = standardize_text(df)
    df = split_genres(df)
    logger.info(f"Cleaning complete. Final shape: {df.shape}")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 1: DUPLICATES
# ─────────────────────────────────────────────────────────────
def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove fully duplicate rows and duplicate show_id entries.

    Keeps the first occurrence of each duplicate.
    """
    before = len(df)
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=["show_id"], keep="first")
    removed = before - len(df)
    logger.info(f"Dropped {removed} duplicate rows.")
    return df.reset_index(drop=True)


# ─────────────────────────────────────────────────────────────
# STEP 2: DTYPES
# ─────────────────────────────────────────────────────────────
def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correct column data types.

    - release_year → Int64 (nullable integer)
    - show_id, type, title, director, cast, country,
      rating, duration, listed_in, description → string (nullable)
    """
    # Nullable integer for release_year
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")

    # String columns
    str_cols = ["show_id", "type", "title", "director", "cast",
                "country", "rating", "duration", "listed_in", "description"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype("string")

    logger.info("Fixed column dtypes.")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 3: DATE_ADDED
# ─────────────────────────────────────────────────────────────
def parse_date_added(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse date_added from string to datetime (UTC-naive).

    Handles formats like 'January 1, 2020' and 'September 25, 2021'.
    Rows that cannot be parsed are left as NaT.
    """
    df["date_added"] = pd.to_datetime(
        df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce"
    )
    n_failed = df["date_added"].isna().sum()
    logger.info(f"Parsed date_added. {n_failed} rows have NaT (could not be parsed).")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 4: DURATION
# ─────────────────────────────────────────────────────────────
def parse_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split the 'duration' column into two numeric columns:
    - duration_minutes (int) for Movies
    - duration_seasons (int) for TV Shows

    The original 'duration' column is retained.
    """
    df["duration"] = df["duration"].fillna("").astype(str)

    movies_mask = df["type"] == "Movie"
    shows_mask  = df["type"] == "TV Show"

    def _extract_int(series: pd.Series, pattern: str) -> pd.Series:
        return series.str.extract(pattern, expand=False).astype(float)

    df["duration_minutes"] = pd.NA
    df["duration_seasons"] = pd.NA

    df.loc[movies_mask, "duration_minutes"] = _extract_int(
        df.loc[movies_mask, "duration"], r"(\d+)\s*min"
    )
    df.loc[shows_mask, "duration_seasons"] = _extract_int(
        df.loc[shows_mask, "duration"], r"(\d+)\s*Season"
    )

    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce").astype("Int64")
    df["duration_seasons"] = pd.to_numeric(df["duration_seasons"], errors="coerce").astype("Int64")

    logger.info("Parsed duration into duration_minutes and duration_seasons.")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 5: COUNTRY NORMALIZATION
# ─────────────────────────────────────────────────────────────
COUNTRY_CORRECTIONS: dict[str, str] = {
    "United States":         "United States",
    "USA":                   "United States",
    "US":                    "United States",
    "UK":                    "United Kingdom",
    "Great Britain":         "United Kingdom",
    "West Germany":          "Germany",
    "Soviet Union":          "Russia",
}


def normalize_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the 'country' column:
    - Strip leading/trailing whitespace from each country in multi-valued cells.
    - Apply known country name corrections.
    - Keep multiple countries as comma-separated string (for later splitting).
    """
    def _clean_country_cell(val: str) -> str:
        if pd.isna(val) or val == "":
            return val
        countries = [c.strip() for c in str(val).split(",")]
        countries = [COUNTRY_CORRECTIONS.get(c, c) for c in countries]
        return ", ".join(countries)

    df["country"] = df["country"].apply(_clean_country_cell)
    logger.info("Normalized country names.")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 6: RATINGS
# ─────────────────────────────────────────────────────────────
RATING_MAP: dict[str, str] = {
    "66 min":  None,   # misclassified duration values
    "74 min":  None,
    "84 min":  None,
    "UR":      "NR",   # Unrated = Not Rated
}


def standardize_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the 'rating' column:
    - Replace known misclassified values (e.g., duration strings) with NaN.
    - Unify 'UR' → 'NR'.
    - Strip whitespace.
    """
    df["rating"] = df["rating"].str.strip()
    df["rating"] = df["rating"].replace(RATING_MAP)
    # Remove any remaining duration-like entries
    df["rating"] = df["rating"].where(
        ~df["rating"].str.match(r"^\d+\s*min$", na=False), other=None
    )
    logger.info("Standardized ratings.")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 7: MISSING VALUES
# ─────────────────────────────────────────────────────────────
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values per column using domain-appropriate strategies:

    - director     → fill with 'Unknown Director'
    - cast         → fill with 'Unknown Cast'
    - country      → fill with 'Unknown'
    - date_added   → left as NaT (cannot impute date without context)
    - rating       → fill with 'Not Rated'
    - duration     → left as-is (extracted columns handle nulls)

    Also adds boolean flags for originally-missing columns:
    - director_missing, cast_missing, country_missing
    """
    # Flags before filling
    df["director_missing"] = df["director"].isna()
    df["cast_missing"]     = df["cast"].isna()
    df["country_missing"]  = df["country"].isna()
    df["rating_missing"]   = df["rating"].isna()

    # Fill
    df["director"] = df["director"].fillna("Unknown Director")
    df["cast"]     = df["cast"].fillna("Unknown Cast")
    df["country"]  = df["country"].fillna("Unknown")
    df["rating"]   = df["rating"].fillna("Not Rated")

    logger.info("Handled missing values.")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 8: TEXT STANDARDIZATION
# ─────────────────────────────────────────────────────────────
def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize text fields:
    - Strip extra whitespace from title, director, cast, listed_in.
    - Title-case the 'type' column.
    - Remove leading/trailing commas from listed_in.
    """
    str_cols = ["title", "director", "cast", "listed_in", "description"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].str.strip()

    df["type"] = df["type"].str.strip().str.title()
    df["listed_in"] = df["listed_in"].str.strip().str.strip(",")

    logger.info("Standardized text fields.")
    return df


# ─────────────────────────────────────────────────────────────
# STEP 9: GENRE SPLITTING
# ─────────────────────────────────────────────────────────────
def split_genres(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split the 'listed_in' column into a Python list stored as 'genres'.
    Each genre is stripped of whitespace.

    The original 'listed_in' column is retained.
    """
    df["genres"] = df["listed_in"].apply(
        lambda x: [g.strip() for g in str(x).split(",") if g.strip()] if pd.notna(x) else []
    )
    logger.info("Split genres into list column 'genres'.")
    return df
