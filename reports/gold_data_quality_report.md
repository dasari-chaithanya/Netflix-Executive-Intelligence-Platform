# Data Quality Report: Gold Stage
**Generated At:** 2026-06-25 20:49:23

## Summary
- **Total Records:** 8,807
- **Total Columns:** 27
- **Memory Usage:** 13.23 MB

## Column Level Quality
| Column | Null Count | Null % | Unique Values | DType |
|---|---|---|---|---|
| `show_id` | 0 | 0.00% | 8807 | `object` |
| `type` | 0 | 0.00% | 2 | `object` |
| `title` | 0 | 0.00% | 8806 | `object` |
| `director` | 0 | 0.00% | 4529 | `object` |
| `cast` | 0 | 0.00% | 7693 | `object` |
| `country` | 831 | 9.44% | 748 | `object` |
| `date_added` | 10 | 0.11% | 1714 | `datetime64[ns]` |
| `release_year` | 0 | 0.00% | 74 | `int64` |
| `rating` | 0 | 0.00% | 13 | `object` |
| `duration` | 0 | 0.00% | 220 | `object` |
| `listed_in` | 0 | 0.00% | 514 | `object` |
| `description` | 0 | 0.00% | 8775 | `object` |
| `duration_mins` | 2,676 | 30.38% | 205 | `float64` |
| `duration_seasons` | 6,131 | 69.62% | 15 | `float64` |
| `genres` | 0 | 0.00% | N/A (List) | `object` |
| `genre_count` | 0 | 0.00% | 3 | `int64` |
| `countries` | 0 | 0.00% | N/A (List) | `object` |
| `country_count` | 0 | 0.00% | 11 | `int64` |
| `director_list` | 0 | 0.00% | N/A (List) | `object` |
| `director_count` | 0 | 0.00% | 13 | `int64` |
| `cast_list` | 0 | 0.00% | N/A (List) | `object` |
| `cast_count` | 0 | 0.00% | 45 | `int64` |
| `release_decade` | 0 | 0.00% | 10 | `int64` |
| `catalog_age` | 0 | 0.00% | 74 | `int64` |
| `month_added` | 10 | 0.11% | 12 | `float64` |
| `year_added` | 10 | 0.11% | 14 | `float64` |
| `weekday_added` | 10 | 0.11% | 7 | `object` |

## Validation Status
✅ PASS - Schema Validated
✅ PASS - Null Thresholds Respected