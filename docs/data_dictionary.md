# Data Dictionary

This outlines the schema contract for the production `netflix_features.parquet` file output by the ETL pipeline.

| Column | Data Type | Nullable | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `show_id` | String | No | Unique identifier | `s1` |
| `type` | String | No | Content type | `Movie`, `TV Show` |
| `title` | String | No | Name of the asset | `Inception` |
| `country` | String | Yes | Production origin (comma separated) | `United States, India` |
| `date_added` | Datetime | Yes | Date ingested to platform | `2021-09-24` |
| `release_year` | Int32 | No | Year of original broadcast | `2010` |
| `rating` | String | Yes | Content maturity rating | `TV-MA` |
| `duration` | String | Yes | Length (minutes or seasons) | `90 min`, `2 Seasons` |
| `genres` | String | Yes | Categorical classification | `Action, Drama` |

> **Note**: This file is read once into memory by `app/data/loader.py` and cached for the duration of the user session.
