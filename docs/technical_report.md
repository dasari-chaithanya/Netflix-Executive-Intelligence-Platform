# Technical Report: Netflix Content Strategy Analysis

## 1. Project Architecture
The project follows a modular, reproducible data engineering pipeline:
* `src/config.py`: Single source of truth for paths, parameters, and KPI definitions.
* `src/cleaning.py`: Standardizes data, handles nulls, and normalizes formats.
* `src/features.py`: Derives 12 analytical features from raw attributes.
* `src/visualization.py`: Generates 35 standardized charts matching Netflix brand colors.
* `src/utils.py`: Helper functions for I/O and KPI calculations.

## 2. Data Engineering Pipeline
The dataset underwent a rigorous 9-step cleaning process:
1. **Deduplication**: Removed exact row duplicates and redundant `show_id` entries.
2. **Type Casting**: Enforced appropriate string, numeric, and datetime data types.
3. **Date Parsing**: Converted textual dates into datetime objects for temporal analysis.
4. **Duration Splitting**: Split mixed-format `duration` into `duration_minutes` (movies) and `duration_seasons` (TV).
5. **Country Normalization**: Standardized naming conventions (e.g., 'West Germany' -> 'Germany').
6. **Rating Standardization**: Corrected misplaced duration values in rating columns and mapped Unrated (UR/NR) uniformly.
7. **Missing Values**: Imputed categorical nulls (Director, Cast, Country) with 'Unknown' rather than dropping rows, preserving temporal and genre data.
8. **Text Stripping**: Removed leading/trailing whitespace.
9. **Genre Splitting**: Converted comma-separated string genres into list types for explode operations.

## 3. Feature Engineering
12 derived features were created to enable deeper analysis:
* **Temporal**: `release_decade`, `year_added`, `month_added`, `weekday_added`, `movie_age`
* **Categorical**: `duration_category`, `primary_genre`, `is_movie`
* **Count-based**: `genre_count`, `country_count`, `director_count`, `cast_count`

## 4. Analytical Tools
* **Jupyter Notebooks**: Documented, step-by-step EDA execution.
* **Plotly & Seaborn**: Static and interactive charting libraries.
* **Streamlit**: Multi-page interactive application for stakeholder presentation.
* **Pytest**: Automated testing of cleaning and feature engineering logic.
