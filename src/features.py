"""
features.py
===========
All feature engineering functions for the Netflix Content Strategy Analysis project.
Import these functions in notebooks/03_feature_engineering.ipynb.
"""

from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd
import numpy as np

from src.config import (
    MOVIE_DURATION_BINS, MOVIE_DURATION_LABELS,
    TV_SEASON_BINS, TV_SEASON_LABELS,
    FEATURES_CSV, FEATURES_PARQUET, POWERBI_CSV,
)

logger = logging.getLogger(__name__)

CURRENT_YEAR = datetime.now().year


# ─────────────────────────────────────────────────────────────
# PIPELINE ENTRY POINT
# ─────────────────────────────────────────────────────────────
def run_feature_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full feature engineering pipeline.

    All 12 locked engineered features:
      release_decade, movie_age, year_added, month_added,
      weekday_added, duration_category, primary_genre,
      genre_count, country_count, director_count,
      cast_count, is_movie

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned Netflix dataset (output of cleaning.run_cleaning_pipeline).

    Returns
    -------
    pd.DataFrame
        Dataset with all engineered features appended.
    """
    logger.info("Starting feature engineering pipeline …")
    df = df.copy()
    df = add_release_decade(df)
    df = add_movie_age(df)
    df = add_date_added_features(df)
    df = add_duration_category(df)
    df = add_genre_features(df)
    df = add_country_count(df)
    df = add_cast_director_counts(df)
    df = add_is_movie_flag(df)
    logger.info(f"Feature engineering complete. Final shape: {df.shape}")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURE: RELEASE DECADE
# ─────────────────────────────────────────────────────────────
def add_release_decade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive 'release_decade' from 'release_year'.
    Values: '1940s', '1950s', … '2020s', or 'Unknown'.
    """
    def _to_decade(year):
        if pd.isna(year):
            return "Unknown"
        return f"{(int(year) // 10) * 10}s"

    df["release_decade"] = df["release_year"].apply(_to_decade)
    logger.info("Added: release_decade")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURE: MOVIE AGE
# ─────────────────────────────────────────────────────────────
def add_movie_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive 'movie_age' as (CURRENT_YEAR − release_year).
    Negative values (future releases) are set to 0.
    """
    df["movie_age"] = (CURRENT_YEAR - df["release_year"].astype(float)).clip(lower=0)
    df["movie_age"] = df["movie_age"].where(df["release_year"].notna(), other=pd.NA)
    df["movie_age"] = df["movie_age"].astype("Int64")
    logger.info("Added: movie_age")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURES: DATE ADDED (year, month, weekday)
# ─────────────────────────────────────────────────────────────
def add_date_added_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive three features from 'date_added':
    - year_added   : integer year
    - month_added  : full month name (e.g., 'January')
    - weekday_added: full weekday name (e.g., 'Friday')
    """
    df["year_added"]    = df["date_added"].dt.year.astype("Int64")
    df["month_added"]   = df["date_added"].dt.month_name()
    df["weekday_added"] = df["date_added"].dt.day_name()
    logger.info("Added: year_added, month_added, weekday_added")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURE: DURATION CATEGORY
# ─────────────────────────────────────────────────────────────
def add_duration_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize content by duration:
    - Movies → Very Short / Short / Medium / Long / Very Long
    - TV Shows → Mini-Series / Short / Medium / Long
    """
    movie_mask = df["type"] == "Movie"
    show_mask  = df["type"] == "TV Show"

    df["duration_category"] = pd.NA

    df.loc[movie_mask, "duration_category"] = pd.cut(
        df.loc[movie_mask, "duration_minutes"].astype(float),
        bins=MOVIE_DURATION_BINS,
        labels=MOVIE_DURATION_LABELS,
        right=False,
    ).astype("string")

    df.loc[show_mask, "duration_category"] = pd.cut(
        df.loc[show_mask, "duration_seasons"].astype(float),
        bins=TV_SEASON_BINS,
        labels=TV_SEASON_LABELS,
        right=False,
    ).astype("string")

    logger.info("Added: duration_category")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURES: GENRE (primary_genre, genre_count)
# ─────────────────────────────────────────────────────────────
def add_genre_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive two genre features:
    - primary_genre : first genre in the genres list
    - genre_count   : number of genres listed
    """
    df["primary_genre"] = df["genres"].apply(
        lambda g: g[0] if isinstance(g, list) and len(g) > 0 else pd.NA
    )
    df["genre_count"] = df["genres"].apply(
        lambda g: len(g) if isinstance(g, list) else 0
    ).astype("Int64")
    logger.info("Added: primary_genre, genre_count")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURE: COUNTRY COUNT
# ─────────────────────────────────────────────────────────────
def add_country_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive 'country_count': number of countries listed per title.
    'Unknown' is treated as 0 countries.
    """
    def _count_countries(val: str) -> int:
        if pd.isna(val) or str(val).strip() in ("", "Unknown"):
            return 0
        return len([c for c in str(val).split(",") if c.strip()])

    df["country_count"] = df["country"].apply(_count_countries).astype("Int64")
    logger.info("Added: country_count")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURES: DIRECTOR COUNT, CAST COUNT
# ─────────────────────────────────────────────────────────────
def add_cast_director_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive:
    - director_count : number of directors listed
    - cast_count     : number of cast members listed

    'Unknown Director' / 'Unknown Cast' are treated as 0.
    """
    def _count_people(val: str, unknown_label: str) -> int:
        if pd.isna(val) or str(val).strip() == unknown_label:
            return 0
        return len([p for p in str(val).split(",") if p.strip()])

    df["director_count"] = df["director"].apply(
        lambda x: _count_people(x, "Unknown Director")
    ).astype("Int64")

    df["cast_count"] = df["cast"].apply(
        lambda x: _count_people(x, "Unknown Cast")
    ).astype("Int64")

    logger.info("Added: director_count, cast_count")
    return df


# ─────────────────────────────────────────────────────────────
# FEATURE: IS_MOVIE FLAG
# ─────────────────────────────────────────────────────────────
def add_is_movie_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Derive boolean flag 'is_movie' (True for Movies, False for TV Shows)."""
    df["is_movie"] = df["type"] == "Movie"
    logger.info("Added: is_movie")
    return df


# ─────────────────────────────────────────────────────────────
# POWER BI EXPORT
# ─────────────────────────────────────────────────────────────
def prepare_powerbi_export(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a flat, Power BI-compatible version of the dataset.

    - Converts list columns to comma-separated strings.
    - Drops boolean flag columns not needed in BI.
    - Ensures all columns are primitive types.
    """
    pbi = df.copy()

    # Convert list column to string
    if "genres" in pbi.columns:
        pbi["genres"] = pbi["genres"].apply(
            lambda g: ", ".join(g) if isinstance(g, list) else ""
        )

    # Drop internal flag columns
    drop_cols = ["director_missing", "cast_missing", "country_missing", "rating_missing"]
    pbi = pbi.drop(columns=[c for c in drop_cols if c in pbi.columns])

    return pbi
