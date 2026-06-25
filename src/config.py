"""
config.py
=========
Central configuration for the Netflix Content Strategy Analysis project.
All paths, constants, color palettes, and business KPI definitions live here.
Import this module instead of hardcoding any values.
"""

from pathlib import Path

# ─────────────────────────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────
# DATA PATHS
# ─────────────────────────────────────────────────────────────
DATA_DIR        = ROOT_DIR / "data"
RAW_DIR         = DATA_DIR / "raw"
PROCESSED_DIR   = DATA_DIR / "processed"

RAW_CSV          = RAW_DIR  / "netflix_titles.csv"
CLEANED_CSV      = PROCESSED_DIR / "netflix_cleaned.csv"
CLEANED_PARQUET  = PROCESSED_DIR / "netflix_cleaned.parquet"
FEATURES_CSV     = PROCESSED_DIR / "netflix_features.csv"
FEATURES_PARQUET = PROCESSED_DIR / "netflix_features.parquet"
POWERBI_CSV      = PROCESSED_DIR / "netflix_powerbi.csv"

# ─────────────────────────────────────────────────────────────
# OUTPUT PATHS
# ─────────────────────────────────────────────────────────────
IMAGES_DIR       = ROOT_DIR / "images"
CHARTS_DIR       = IMAGES_DIR / "charts"
DASHBOARD_DIR    = IMAGES_DIR / "dashboard"
REPORTS_DIR      = ROOT_DIR / "reports"
DOCS_DIR         = ROOT_DIR / "docs"

# ─────────────────────────────────────────────────────────────
# CHART CATEGORY SUBDIRECTORIES (auto-created on first use)
# ─────────────────────────────────────────────────────────────
CHART_CATEGORIES = [
    "overview", "timeline", "country", "genre",
    "ratings", "duration", "directors", "cast",
    "missing", "features"
]

# ─────────────────────────────────────────────────────────────
# COLOR PALETTE  (neutral-first, red only for emphasis)
# ─────────────────────────────────────────────────────────────
NETFLIX_RED     = "#E50914"
ACCENT_DARK     = "#221F1F"
ACCENT_LIGHT    = "#F5F5F1"
GRAY_DARK       = "#564D4D"
GRAY_MID        = "#8A8A8A"
GRAY_LIGHT      = "#D9D9D9"

# Sequential palette — use for bar/line charts
SEQ_PALETTE = [
    "#2E4057", "#048A81", "#54C6EB", "#8EE3EF",
    "#CAF0F8", "#EF8354", "#BFC0C0", "#3D405B"
]

# Diverging palette — use for heatmaps
DIV_PALETTE = "RdGy"

# Netflix brand palette (use sparingly — highlight only)
BRAND_PALETTE = [NETFLIX_RED, ACCENT_DARK, GRAY_MID, ACCENT_LIGHT]

# Plotly template
PLOTLY_TEMPLATE = "plotly_dark"

# ─────────────────────────────────────────────────────────────
# TYPOGRAPHY
# ─────────────────────────────────────────────────────────────
FONT_FAMILY   = "Inter, Arial, sans-serif"
TITLE_SIZE    = 18
SUBTITLE_SIZE = 13
LABEL_SIZE    = 11
TICK_SIZE     = 10

# ─────────────────────────────────────────────────────────────
# FIGURE SETTINGS
# ─────────────────────────────────────────────────────────────
FIG_DPI       = 150
FIG_SIZE_SM   = (8, 5)
FIG_SIZE_MD   = (12, 6)
FIG_SIZE_LG   = (16, 8)
FIG_SIZE_WIDE = (18, 6)

# ─────────────────────────────────────────────────────────────
# BUSINESS KPIs (locked — 12 KPIs)
# ─────────────────────────────────────────────────────────────
BUSINESS_KPIS = [
    "Total Titles",
    "Movie vs TV Show Ratio",
    "Average Movie Duration (min)",
    "Average TV Show Seasons",
    "Content Growth Rate (YoY %)",
    "Top Producing Country",
    "Top Genre",
    "Content Added per Year",
    "Median Movie Age (years)",
    "Genre Diversity (unique genres)",
    "Country Diversity (unique countries)",
    "Rating Distribution (% per rating)",
]

# ─────────────────────────────────────────────────────────────
# CHART PLAN (35 locked visualizations)
# ─────────────────────────────────────────────────────────────
CHART_PLAN = {
    "overview":  5,
    "timeline":  5,
    "country":   5,
    "genre":     5,
    "ratings":   4,
    "duration":  3,
    "directors": 2,
    "cast":      2,
    "missing":   2,
    "features":  2,
}
assert sum(CHART_PLAN.values()) == 35, "Chart plan must total exactly 35."

# ─────────────────────────────────────────────────────────────
# FEATURE COLUMNS (locked)
# ─────────────────────────────────────────────────────────────
ENGINEERED_FEATURES = [
    "release_decade",
    "movie_age",
    "year_added",
    "month_added",
    "weekday_added",
    "duration_category",
    "primary_genre",
    "genre_count",
    "country_count",
    "director_count",
    "cast_count",
    "is_movie",
]

# ─────────────────────────────────────────────────────────────
# RATINGS GROUPINGS
# ─────────────────────────────────────────────────────────────
RATING_GROUPS = {
    "Kids":   ["G", "TV-G", "TV-Y", "TV-Y7", "TV-Y7-FV"],
    "Family": ["PG", "TV-PG"],
    "Teen":   ["PG-13", "TV-14"],
    "Mature": ["R", "TV-MA", "NC-17"],
    "Unrated": ["NR", "UR"],
}

# ─────────────────────────────────────────────────────────────
# DURATION CATEGORIES
# ─────────────────────────────────────────────────────────────
MOVIE_DURATION_BINS   = [0, 60, 90, 120, 180, 9999]
MOVIE_DURATION_LABELS = ["Very Short (<60)", "Short (60-90)", "Medium (90-120)", "Long (120-180)", "Very Long (180+)"]

TV_SEASON_BINS   = [0, 1, 3, 6, 99]
TV_SEASON_LABELS = ["Mini-Series (1)", "Short (2-3)", "Medium (4-6)", "Long (7+)"]

# ─────────────────────────────────────────────────────────────
# HELPER — ensure output directories exist
# ─────────────────────────────────────────────────────────────
def ensure_dirs() -> None:
    """Create all output directories if they don't already exist."""
    dirs = [PROCESSED_DIR, CHARTS_DIR, DASHBOARD_DIR, REPORTS_DIR, DOCS_DIR]
    for cat in CHART_CATEGORIES:
        dirs.append(CHARTS_DIR / cat)
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
