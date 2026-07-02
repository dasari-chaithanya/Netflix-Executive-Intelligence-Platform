# KPI Dictionary

This document centralizes the business logic utilized in the Netflix Content Strategy Platform. All logic lives in `app/business/rules.py` and `src/kpi_engine/`.

## 1. Catalog Freshness
- **Definition**: The percentage of the total active catalog that was added to the platform within the trailing 24 months.
- **Why it matters**: Indicates whether the platform is heavily reliant on an aging back-catalog or is successfully injecting new capital into recent acquisitions.
- **Thresholds**: 
  - `Green`: > 35%
  - `Orange`: 25% - 35%
  - `Red`: < 25%

## 2. Average Content Age
- **Definition**: The average number of years since the original theatrical/broadcast release of the title.
- **Why it matters**: Determines if the catalog appeals to audiences looking for modern releases versus classic/legacy titles.
- **Thresholds**: 
  - `Green`: < 4.5 years
  - `Orange`: 4.5 - 6.0 years
  - `Red`: > 6.0 years

## 3. Mature Audience Share
- **Definition**: The percentage of the catalog rated TV-MA or R.
- **Why it matters**: Content safety and demographic targeting. Ensures the platform doesn't accidentally shift toward an overly mature or overly restrictive catalog relative to its subscriber base.
- **Thresholds**: 
  - `Green`: > 40%
  - `Orange`: 25% - 40%
  - `Red`: < 25%
