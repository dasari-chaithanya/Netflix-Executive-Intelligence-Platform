"""
utils.py
========
Shared utility functions for the Netflix Content Strategy Analysis project.
"""

from __future__ import annotations

import json
import time
import logging
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np

from src.config import CHARTS_DIR, CHART_CATEGORIES, ensure_dirs

# ─────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# I/O HELPERS
# ─────────────────────────────────────────────────────────────
def load_csv(path: Path | str, **kwargs) -> pd.DataFrame:
    """Load a CSV with logging and basic validation."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path, **kwargs)
    logger.info(f"Loaded {path.name}: {df.shape[0]:,} rows × {df.shape[1]} cols")
    return df


def load_parquet(path: Path | str, **kwargs) -> pd.DataFrame:
    """Load a Parquet file with logging."""
    path = Path(path)
    df = pd.read_parquet(path, **kwargs)
    logger.info(f"Loaded {path.name}: {df.shape[0]:,} rows × {df.shape[1]} cols")
    return df


def save_csv(df: pd.DataFrame, path: Path | str, **kwargs) -> None:
    """Save DataFrame to CSV, creating directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, **kwargs)
    logger.info(f"Saved CSV  → {path}  ({df.shape[0]:,} rows)")


def save_parquet(df: pd.DataFrame, path: Path | str, **kwargs) -> None:
    """Save DataFrame to Parquet, creating directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False, **kwargs)
    logger.info(f"Saved Parquet → {path}  ({df.shape[0]:,} rows)")


# ─────────────────────────────────────────────────────────────
# DATAFRAME INSPECTION
# ─────────────────────────────────────────────────────────────
def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with missing value counts and percentages."""
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    summary = pd.DataFrame({
        "missing_count": missing,
        "missing_pct":   pct,
        "dtype":         df.dtypes,
    })
    return summary[summary["missing_count"] > 0].sort_values("missing_count", ascending=False)


def duplicate_summary(df: pd.DataFrame, subset: list[str] | None = None) -> dict[str, int]:
    """Return count of fully duplicate rows and subset-duplicate rows."""
    full_dupes = df.duplicated().sum()
    subset_dupes = df.duplicated(subset=subset).sum() if subset else None
    return {"full_duplicates": int(full_dupes), "subset_duplicates": subset_dupes}


def quick_profile(df: pd.DataFrame) -> None:
    """Print a quick data profile to console."""
    print(f"{'─'*50}")
    print(f"Shape          : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory usage   : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Missing cells  : {df.isnull().sum().sum():,}")
    print(f"Duplicate rows : {df.duplicated().sum():,}")
    print(f"{'─'*50}")
    print(df.dtypes.to_string())
    print(f"{'─'*50}")


# ─────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────
def chart_path(category: str, filename: str) -> Path:
    """
    Return the full path for a chart file.

    Parameters
    ----------
    category : str
        One of the locked chart categories (see config.CHART_CATEGORIES).
    filename : str
        Filename including extension, e.g. 'movies_vs_tv.png'.
    """
    if category not in CHART_CATEGORIES:
        raise ValueError(f"Unknown chart category '{category}'. Must be one of {CHART_CATEGORIES}")
    ensure_dirs()
    return CHARTS_DIR / category / filename


def save_fig(fig, category: str, filename: str, dpi: int = 150) -> Path:
    """Save a Matplotlib figure to the appropriate chart subdirectory."""
    import matplotlib.pyplot as plt  # lazy import
    path = chart_path(category, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    logger.info(f"Chart saved → {path.relative_to(path.parents[3])}")
    return path


def save_plotly(fig, category: str, filename: str) -> Path:
    """Save a Plotly figure as a static PNG (requires kaleido)."""
    path = chart_path(category, filename)
    fig.write_image(str(path))
    logger.info(f"Chart saved → {path.relative_to(path.parents[3])}")
    return path


# ─────────────────────────────────────────────────────────────
# KPI COMPUTATION
# ─────────────────────────────────────────────────────────────
def compute_kpis(df: pd.DataFrame) -> dict[str, Any]:
    """
    Compute all 12 locked business KPIs from the features DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The engineered features dataset (netflix_features.csv / .parquet).

    Returns
    -------
    dict[str, Any]
        Dictionary of KPI name → value.
    """
    movies = df[df["type"] == "Movie"]
    shows  = df[df["type"] == "TV Show"]

    # Content growth rate (YoY % change in most recent two full years)
    yearly = df.dropna(subset=["year_added"]).groupby("year_added").size()
    if len(yearly) >= 2:
        last_year  = yearly.iloc[-1]
        prev_year  = yearly.iloc[-2]
        growth_rate = round((last_year - prev_year) / prev_year * 100, 1) if prev_year else None
    else:
        growth_rate = None

    top_country = (
        df["country"].dropna()
        .str.split(",").explode().str.strip()
        .value_counts().idxmax()
        if df["country"].notna().any() else "N/A"
    )

    top_genre = (
        df["primary_genre"].dropna().value_counts().idxmax()
        if "primary_genre" in df.columns and df["primary_genre"].notna().any() else "N/A"
    )

    avg_movie_duration = (
        round(movies["duration_minutes"].mean(), 1)
        if "duration_minutes" in movies.columns else None
    )

    avg_tv_seasons = (
        round(shows["duration_seasons"].mean(), 1)
        if "duration_seasons" in shows.columns else None
    )

    median_movie_age = (
        round(movies["movie_age"].median(), 1)
        if "movie_age" in movies.columns else None
    )

    genre_diversity = (
        df["primary_genre"].nunique()
        if "primary_genre" in df.columns else None
    )

    country_diversity = (
        df["country"].dropna().str.split(",").explode().str.strip().nunique()
        if df["country"].notna().any() else None
    )

    content_added_per_year = (
        round(df.dropna(subset=["year_added"]).groupby("year_added").size().mean(), 1)
        if "year_added" in df.columns else None
    )

    return {
        "Total Titles":                    len(df),
        "Movies":                          len(movies),
        "TV Shows":                        len(shows),
        "Movie vs TV Show Ratio":          f"{len(movies)}:{len(shows)}",
        "Average Movie Duration (min)":    avg_movie_duration,
        "Average TV Show Seasons":         avg_tv_seasons,
        "Content Growth Rate (YoY %)":     growth_rate,
        "Top Producing Country":           top_country,
        "Top Genre":                       top_genre,
        "Content Added per Year (avg)":    content_added_per_year,
        "Median Movie Age (years)":        median_movie_age,
        "Genre Diversity":                 genre_diversity,
        "Country Diversity":               country_diversity,
    }


# ─────────────────────────────────────────────────────────────
# MISC
# ─────────────────────────────────────────────────────────────
def timer(func):
    """Decorator to log function execution time."""
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} completed in {elapsed:.2f}s")
        return result
    return wrapper


def flatten_list(nested: list) -> list:
    """Flatten a list of lists into a single list."""
    return [item for sublist in nested for item in sublist]


def pct_format(value: float, total: float, decimals: int = 1) -> str:
    """Format a value as a percentage string."""
    return f"{value / total * 100:.{decimals}f}%"
