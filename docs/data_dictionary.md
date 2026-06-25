# Data Dictionary
## Netflix Content Strategy Analysis

This document describes every column in the dataset at each stage of the pipeline.

---

## 1. Raw Dataset (`data/raw/netflix_titles.csv`)

Source: [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

| Column | Type | Description | Example | Missing? |
|--------|------|-------------|---------|----------|
| `show_id` | string | Unique identifier for each title | `s1` | No |
| `type` | string | Content type: `Movie` or `TV Show` | `Movie` | No |
| `title` | string | Title of the content | `Inception` | Rare |
| `director` | string | Director name(s), comma-separated | `Christopher Nolan` | ~30% |
| `cast` | string | Cast member names, comma-separated | `Leonardo DiCaprio, Joseph Gordon-Levitt` | ~10% |
| `country` | string | Country/countries of production, comma-separated | `United States, United Kingdom` | ~7% |
| `date_added` | string → datetime | Date the title was added to Netflix | `January 1, 2020` | ~1% |
| `release_year` | integer | Original release year of the content | `2010` | No |
| `rating` | string | Content rating (TV-MA, PG-13, etc.) | `TV-MA` | ~1% |
| `duration` | string | Runtime for movies (min) or seasons for shows | `148 min` / `3 Seasons` | <1% |
| `listed_in` | string | Genres, comma-separated | `Action & Adventure, Sci-Fi & Fantasy` | No |
| `description` | string | Short synopsis of the content | `A thief who steals...` | Rare |

---

## 2. Cleaned Dataset (`data/processed/netflix_cleaned.csv` / `.parquet`)

All raw columns retained, with the following modifications and additions:

| Column | Change | Description |
|--------|--------|-------------|
| `show_id` | Unchanged | Unique identifier |
| `type` | Title-cased | `Movie` / `TV Show` |
| `title` | Stripped | Whitespace removed |
| `director` | Missing filled | `Unknown Director` where null; original values stripped |
| `cast` | Missing filled | `Unknown Cast` where null |
| `country` | Normalized | Country name corrections applied; `Unknown` where null |
| `date_added` | Parsed | Converted to `datetime64` |
| `release_year` | Fixed | Cast to nullable `Int64` |
| `rating` | Standardized | `UR` → `NR`; misclassified duration strings removed |
| `duration` | Cleaned | Stripped |
| `duration_minutes` | **NEW** | Extracted numeric minutes for Movies (Int64) |
| `duration_seasons` | **NEW** | Extracted numeric seasons for TV Shows (Int64) |
| `listed_in` | Stripped | Whitespace and trailing commas removed |
| `genres` | **NEW** | Python list of genres split from `listed_in` |
| `director_missing` | **NEW** | Boolean flag: True if director was originally null |
| `cast_missing` | **NEW** | Boolean flag: True if cast was originally null |
| `country_missing` | **NEW** | Boolean flag: True if country was originally null |
| `rating_missing` | **NEW** | Boolean flag: True if rating was originally null |

---

## 3. Engineered Features Dataset (`data/processed/netflix_features.csv` / `.parquet`)

All cleaned columns retained, with the following engineered features added:

| Feature Column | Type | Description | Example |
|----------------|------|-------------|---------|
| `release_decade` | string | Decade of release year | `2010s` |
| `movie_age` | Int64 | Current year minus release_year | `14` |
| `year_added` | Int64 | Year extracted from date_added | `2021` |
| `month_added` | string | Month name from date_added | `January` |
| `weekday_added` | string | Weekday name from date_added | `Friday` |
| `duration_category` | string | Duration bucket (see below) | `Medium (90-120)` |
| `primary_genre` | string | First genre listed in genres | `Dramas` |
| `genre_count` | Int64 | Number of genres | `3` |
| `country_count` | Int64 | Number of countries listed | `2` |
| `director_count` | Int64 | Number of directors | `1` |
| `cast_count` | Int64 | Number of cast members | `8` |
| `is_movie` | bool | True if type is Movie | `True` |

### Duration Category Definitions

**Movies:**
| Category | Minutes |
|----------|---------|
| Very Short | < 60 min |
| Short | 60–89 min |
| Medium | 90–119 min |
| Long | 120–179 min |
| Very Long | ≥ 180 min |

**TV Shows:**
| Category | Seasons |
|----------|---------|
| Mini-Series | 1 season |
| Short | 2–3 seasons |
| Medium | 4–6 seasons |
| Long | ≥ 7 seasons |

---

## 4. Power BI Export (`data/processed/netflix_powerbi.csv`)

Flat, Power BI-compatible version of the features dataset:
- List columns converted to comma-separated strings.
- Internal boolean flag columns dropped.
- All types are primitives (no Python-specific nullable types).

---

## Rating Definitions

| Rating | Audience |
|--------|----------|
| `G` / `TV-G` | All audiences (General) |
| `TV-Y` / `TV-Y7` | Children under 7 / over 7 |
| `PG` / `TV-PG` | Parental guidance suggested |
| `PG-13` / `TV-14` | Parents cautioned / teens 14+ |
| `R` / `TV-MA` | Restricted / Mature audiences only |
| `NC-17` | Adults only |
| `NR` | Not rated |

---

## Notes

- Multi-valued fields (`director`, `cast`, `country`, `listed_in`) are stored as comma-separated strings throughout the pipeline to maintain CSV compatibility. The `genres` column stores a Python list in Parquet format.
- Titles with `date_added = NaT` are excluded from time-series analyses but included in all catalog-level analyses.
- The `movie_age` feature is computed relative to the project's analysis year (2026).
