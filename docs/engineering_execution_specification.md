# Netflix Content Strategy & Catalog Intelligence Platform
## Engineering Execution Specification (Phase 5)

---

## 1. PROJECT MILESTONES

The project is structured into 6 sequential milestones to ensure risk is mitigated early (Data before UI) and dependencies are strictly respected.

*   **M1: Foundation & DevOps (Days 1-2)**: Setup repo, CI/CD pipelines, styling tools, and design tokens.
*   **M2: Data Engineering & Contracts (Days 3-5)**: Implement ETL pipelines, enforce data contracts, and output validated Parquet files.
*   **M3: KPI Engine & Backend Logic (Days 6-7)**: Implement pure Python functions for KPIs and statistical aggregations.
*   **M4: Core UI Components & State (Days 8-10)**: Build reusable Streamlit components (Cards, Filters) and wire `st.session_state`.
*   **M5: Chart Factory & Dashboard Assembly (Days 11-14)**: Implement Plotly factory functions and assemble the multi-page layout.
*   **M6: Quality, Performance & Launch (Days 15-16)**: E2E testing, performance budgeting, and deployment to Streamlit Community Cloud.

---

## 2. WORK BREAKDOWN STRUCTURE (WBS)

### M1: Foundation & DevOps
**Task ID: M1.1 - Repo Initialization**
*   **Description**: Setup Git, `pyproject.toml`, `requirements.txt`, and standard folder structure.
*   **Dependencies**: None.
*   **Effort**: 0.5 Days.
*   **Deliverables**: GitHub Repo.
*   **Acceptance Criteria (AC)**: `make install` works cleanly on a fresh virtual environment.

**Task ID: M1.2 - CI/CD & Linting Setup**
*   **Description**: Configure GitHub Actions, `.pre-commit-config.yaml`, `ruff`, `black`, `isort`, `mypy`.
*   **Dependencies**: M1.1
*   **Effort**: 0.5 Days.
*   **Deliverables**: CI Pipeline.
*   **AC**: Commits fail if formatting or type hinting is incorrect.

### M2: Data Engineering
**Task ID: M2.1 - ETL Pipeline Implementation**
*   **Description**: Write cleaning and feature engineering scripts to convert raw Kaggle CSV to processed Parquet.
*   **Dependencies**: M1.1
*   **Effort**: 1.5 Days.
*   **Deliverables**: `src/data_pipeline/etl.py`, `processed/netflix_features.parquet`.
*   **AC**: Output file matches Data Contract (Section 3). Zero missing values in primary columns.

### M3: Backend Logic
**Task ID: M3.1 - KPI Engine Implementation**
*   **Description**: Write the pure functions to calculate the 10 locked KPIs.
*   **Dependencies**: M2.1
*   **Effort**: 1.5 Days.
*   **Deliverables**: `src/kpi_engine/metrics.py`.
*   **AC**: 100% unit test coverage for all KPI functions using mock data.

### M4: Frontend Core
**Task ID: M4.1 - Design Token Integration**
*   **Description**: Create `design_tokens.json` and map them to Streamlit's `config.toml`.
*   **Dependencies**: M1.1
*   **Effort**: 0.5 Days.
*   **Deliverables**: Consistent dark mode UI layer.
*   **AC**: App background strictly `#141414`, fonts default to 'Inter'.

**Task ID: M4.2 - Reusable UI Components**
*   **Description**: Build `KPICard`, `FilterDrawer`, `InsightCard`.
*   **Dependencies**: M4.1
*   **Effort**: 2 Days.
*   **Deliverables**: `app/components/*.py`.
*   **AC**: Components render flawlessly with dummy data and respond to screen resizing.

### M5: Assembly
**Task ID: M5.1 - Chart Factory**
*   **Description**: Build the 20 locked Plotly charts conforming to the Chart Spec (Section 5).
*   **Dependencies**: M2.1, M4.1
*   **Effort**: 3 Days.
*   **Deliverables**: `app/charts/*.py`.
*   **AC**: Charts have no gridlines, no default legends, custom tooltips, and scale correctly.

**Task ID: M5.2 - Page Assembly & State Wiring**
*   **Description**: Assemble the 11 pages, inject charts/KPIs, and wire global filters to `st.session_state`.
*   **Dependencies**: M3.1, M4.2, M5.1
*   **Effort**: 2 Days.
*   **Deliverables**: `app/pages/*.py`.
*   **AC**: Changing the "Region" filter instantly updates all charts and KPIs on the current page.

---

## 3. DATA CONTRACT

This contract dictates the exact schema required for `processed/netflix_features.parquet`. If the ETL pipeline deviates, the CI build fails.

| Column Name | Datatype | Nullable | Validation | Source | Used By | Transformation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `show_id` | `str` | No | Unique, `^s\d+$` | raw:`show_id` | All | None |
| `type` | `str` | No | `IN ('Movie', 'TV Show')` | raw:`type` | Filters, Portfolio | None |
| `title` | `str` | No | `len > 0` | raw:`title` | Tooltips | Strip whitespace |
| `director` | `list[str]` | Yes | `len >= 0` | raw:`director` | Filters | Split by `,` |
| `cast` | `list[str]` | Yes | `len >= 0` | raw:`cast` | Filters | Split by `,` |
| `countries` | `list[str]` | No | Must contain valid ISO names | raw:`country` | Expansion | Split, Impute 'Unknown' |
| `date_added` | `datetime` | No | `>= 2008-01-01` | raw:`date_added` | Growth, KPIs | Parse to `pd.to_datetime` |
| `release_year` | `int` | No | `>= 1920` | raw:`release_year` | Growth | Cast to Int |
| `rating` | `str` | No | Valid maturity rating | raw:`rating` | Audience | Standardize UR/NR |
| `duration_mins` | `int` | Yes | `> 0` | raw:`duration` | Quality | Extract int if Movie |
| `duration_seasons` | `int` | Yes | `> 0` | raw:`duration` | Quality | Extract int if TV Show |
| `genres` | `list[str]` | No | Valid genres list | raw:`listed_in` | Genre | Split by `,` |

---

## 4. KPI DICTIONARY

Every KPI is strictly defined to prevent calculation ambiguity.

**1. Catalog Freshness**
*   **Formula**: `(Titles where date_added >= Today - 24 Months) / (Total Titles)`
*   **Units**: Percentage (%)
*   **Display Format**: `42.5%`
*   **Data Source**: `date_added`
*   **Validation**: Must be between 0 and 100.
*   **Business Meaning**: Evaluates if the catalog relies on legacy content or recent acquisitions.

**2. Average Content Age**
*   **Formula**: `Mean(Current_Year - release_year)`
*   **Units**: Years
*   **Display Format**: `8.2 yrs`
*   **Data Source**: `release_year`
*   **Validation**: Must be `> 0`.
*   **Business Meaning**: Determines if Netflix is licensing older studio back-catalogs vs funding new originals.

**3. Series Survival Rate**
*   **Formula**: `(TV Shows where duration_seasons > 1) / (Total TV Shows)`
*   **Units**: Percentage (%)
*   **Display Format**: `34.1%`
*   **Data Source**: `duration_seasons`, `type`
*   **Validation**: Must be between 0 and 100.
*   **Business Meaning**: Indicates the success rate of Netflix series renewals against cancellation thresholds.

---

## 5. CHART SPECIFICATION (Sample Set)

*Developers must adhere strictly to these dimensions for the 20 approved charts.*

**Chart ID: `CHRT-GEO-01` (Global Expansion)**
*   **Business Question**: Which regions are untouched by Netflix production?
*   **Chart Type**: Choropleth Map (Log Scale)
*   **Dataset**: `processed_countries_aggregated`
*   **Dimensions**: `ISO_Alpha_3`
*   **Measures**: `Count(show_id)`
*   **Filters**: `Global Date Range`, `Content Type`
*   **Expected Insight**: Identifies whitespace in emerging markets (e.g., Africa/Eastern Europe).
*   **Recommendation Trigger**: If region volume < 5% but subscriber growth is high -> "Accelerate Local Co-Productions."

**Chart ID: `CHRT-TIM-02` (Growth Analytics)**
*   **Business Question**: Are there seasonal trends in content acquisition?
*   **Chart Type**: Calendar Heatmap
*   **Dataset**: `processed_features`
*   **Dimensions**: `Month(date_added)`, `Year(date_added)`
*   **Measures**: `Count(show_id)`
*   **Filters**: `Content Type`, `Genre`
*   **Expected Insight**: Content dumping typically occurs in Q4 to capture holiday viewership.

---

## 6. COMPONENT DEPENDENCY GRAPH

```text
Global Session State
 ├── Filters (`date_range`, `type`, `genre`)
 │
 ├──> Page Router
 │     ├──> 01_Executive_Dashboard
 │     │     ├── KPI Engine (Injects filtered DF)
 │     │     │    └── KPICard (Renders output)
 │     │     └── Chart Factory (Injects filtered DF)
 │     │          └── ChartContainer (Renders Plotly Figure)
 │     │
 │     └──> 02_Genre_Strategy
 │           ├── KPI Engine
 │           ├── Chart Factory
 │           └── InsightCard (Static strategic text mapping to KPIs)
```

---

## 7. ENGINEERING TIMELINE

A highly realistic 16-day execution plan (assuming 1 Senior Engineer).

*   **Day 1**: Repo Setup, CI/CD, Linters, Design Tokens JSON.
*   **Day 2-3**: Data ETL Pipeline, Pandas transformations.
*   **Day 4**: Data Validation tests, Data Dictionary generation.
*   **Day 5**: KPI Engine (Pure Python) and unit testing.
*   **Day 6-7**: Streamlit UI Shell, Routing, Sidebar, Global State setup.
*   **Day 8-9**: Reusable UI Components (Cards, Containers, Drawers).
*   **Day 10-12**: Chart Factory (Plotly generation, theming, tooltips).
*   **Day 13-14**: Dashboard Assembly (Connecting data to UI across 11 pages).
*   **Day 15**: Optimization (Caching, lazy loading tabs, profiling memory).
*   **Day 16**: Final QA, GitHub deployment, Streamlit Cloud deployment.

---

## 8. RISK REGISTER

| Risk Type | Description | Mitigation Plan |
| :--- | :--- | :--- |
| **Technical** | Exploding `genres` and `countries` lists creates massive RAM spikes. | Pre-aggregate data into smaller summary parquet files during ETL; do not explode on the fly in Streamlit. |
| **Performance** | Streamlit reruns the whole page on every filter change, causing 3-second delays. | Wrap visualizations in `@st.experimental_fragment` so only the charts update, bypassing full page reloads. |
| **Data Quality** | Kaggle dataset contains unstructured, dirty text in `duration`. | Write aggressive Regex extraction in the ETL phase and unit test against edge cases (`"3 Seasons"`, `"90 min"`). |
| **UX** | Plotly charts scaling poorly on mobile displays. | Disable Plotly zoom/pan on mobile; force legends to the bottom; rely on tap-to-tooltip. |

---

## 9. QUALITY GATES

*   **Gate 1 (Post-ETL)**: Parquet files must load into Pandas in `< 0.2s`. Zero nulls in primary dimensions.
*   **Gate 2 (Post-Backend)**: `pytest` coverage > 85%. All KPIs calculate in `< 0.05s`.
*   **Gate 3 (Post-Frontend)**: Streamlit app launches successfully locally. Lighthouse accessibility score > 90.
*   **Gate 4 (Pre-Launch)**: Entire app deployed to Cloud. Initial load `< 1.5s`. Total memory footprint `< 250MB`.

---

## 10. DEFINITION OF DONE (DoD)

A task or feature is officially "Done" only when:
1.  Code is written and conforms to PEP 8 (`black`, `ruff`).
2.  Type hints are complete and pass `mypy`.
3.  Unit tests are written and passing in GitHub Actions.
4.  Data Contracts are respected (no schema violations).
5.  UI Components match the exact visual specs defined in the Design Tokens (colors, spacing, typography).
6.  Performance falls within the stated budget (Filters resolve in < 300ms).
7.  The feature is merged to the `main` branch via Pull Request.
