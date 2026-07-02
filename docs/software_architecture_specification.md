# Netflix Content Strategy & Catalog Intelligence Platform
## Software Architecture Specification

---

## SECTION 1 — REPOSITORY ARCHITECTURE

A strict separation of concerns ensures the project remains scalable, testable, and legible for both engineers and recruiters reviewing the portfolio.

```text
netflix-catalog-intelligence/
├── data/
│   ├── raw/                 # Immutable source datasets
│   ├── processed/           # Cleaned datasets, feature tables, aggregations
│   └── tests/               # Mock data for unit testing
├── src/
│   ├── config/              # Constants, theme colors, layout dimensions
│   ├── data_pipeline/       # ETL scripts: clean, feature engineer, aggregate
│   ├── kpi_engine/          # Pure functions for business metrics calculation
│   └── utils/               # Generic helpers (formatting, I/O, error handlers)
├── app/
│   ├── main.py              # Streamlit entry point (routing & shell)
│   ├── pages/               # Streamlit multi-page routing files (01_Dashboard.py)
│   ├── components/          # Reusable UI elements (cards, containers)
│   ├── charts/              # Plotly chart generation factory functions
│   └── state/               # Session state initializers and mutators
├── tests/
│   ├── unit/                # Testing pure Python logic (KPIs, cleaning)
│   ├── integration/         # Testing ETL pipeline end-to-end
│   └── ui/                  # Testing Streamlit rendering logic
├── docs/                    # Design specs, blueprints, data dictionaries
├── assets/                  # CSS overrides, branding, static images
├── notebooks/               # EDA and ad-hoc analysis (for portfolio depth)
├── reports/                 # Exported PDF outputs and snapshots
├── requirements.txt         # Pinned dependencies
├── Makefile                 # CLI commands (make run, make test, make clean)
└── README.md                # Recruiter-optimized project landing page
```

---

## SECTION 2 — APPLICATION ARCHITECTURE

The application follows a strictly layered architecture to decouple UI rendering from data processing.

1.  **Presentation Layer (`app/pages/`, `app/components/`)**: Responsible solely for rendering Streamlit UI elements, reading from Session State, and handling layout constraints.
2.  **State Layer (`app/state/`)**: Manages `st.session_state` mutations. All filters update this layer, which triggers UI reruns.
3.  **Visualization Layer (`app/charts/`)**: Translates Pandas DataFrames into Plotly objects. Applies strict theming and hover templates.
4.  **Business Layer (`src/kpi_engine/`)**: Calculates core derived metrics (e.g., Catalog Freshness, Series Survival Rate). Pure Python functions.
5.  **Data Layer (`src/data_pipeline/`)**: Handles schema validation, filtering, and grouped aggregations before sending data to the Business/Viz layers.
6.  **Storage Layer (`data/`)**: Manages the underlying CSV/Parquet files. Treated as read-only by the application.

---

## SECTION 3 — STREAMLIT ARCHITECTURE

To avoid fighting Streamlit’s execution model, the architecture adheres to these principles:
*   **Data Loading**: Base datasets are loaded *once* using `@st.cache_data`.
*   **Filtering via Session State**: Global filters exist in the sidebar or a fixed top container. Changing a filter updates `st.session_state`, automatically triggering a top-down script rerun with the new context.
*   **Layouts**: Strict use of `st.columns` for grid layouts and `st.container` to group related metrics and charts.
*   **Page Organization**: `st.tabs` are used for deep-dives (e.g., viewing underlying data tables) without extending page length.
*   **No DOM Manipulation**: Avoid custom CSS transitions or JS hacks. Rely entirely on Streamlit's native responsive rendering.

---

## SECTION 4 — COMPONENT ARCHITECTURE

UI logic must be modular to prevent massive, unreadable page files.

*   `KPICard(title, metric, delta, tooltip_text)`: Renders a standardized `st.metric` wrapped in a custom container for consistent spacing.
*   `InsightCard(type, summary, detail)`: Renders text insights using markdown. Automatically applies colored tags (Info, Warning, Success) based on `type`.
*   `ChartContainer(title, business_question, chart_figure)`: Standardized wrapper. Renders a header, a subheader (the question), and the Plotly figure via `st.plotly_chart(use_container_width=True)`.
*   `FilterDrawer()`: Aggregates `st.multiselect` and `st.slider` widgets. Returns a dictionary of active filter criteria.
*   `EmptyState(message)`: Standardized warning using `st.info()` when filtered data yields zero rows.

---

## SECTION 5 — DATA PIPELINE

ETL runs *prior* to the Streamlit app launching, ensuring the dashboard only reads optimized files.

1.  **Raw CSV Load**: Read Kaggle dataset.
2.  **Cleaning (`cleaning.py`)**: Handle nulls (e.g., fill 'Unknown' for Director), enforce dtypes, parse dates, strip whitespace.
3.  **Feature Engineering (`features.py`)**: 
    *   Extract Release Decade.
    *   Split 'duration' into `duration_minutes` (Int) and `duration_seasons` (Int).
    *   Explode comma-separated genres/countries into list formats.
4.  **Aggregations (`aggregations.py`)**: Pre-compute heavy groupings (e.g., Country x Year x Genre counts) and save to Parquet.
5.  **Dashboard Integration**: App reads `processed/netflix_features.parquet` instantly via caching.

---

## SECTION 6 — STATE MANAGEMENT

Explicitly defining what belongs in `st.session_state` prevents race conditions and memory bloat.

*   **Global State**: `st.session_state['global_date_range']`, `st.session_state['content_type_filter']`. Persists across multi-page navigation.
*   **Page State**: Transitory states like the active tab in a deep-dive view. Stateless; handled by Streamlit's native widget returns.
*   **Data State**: Managed entirely by `@st.cache_data`. Raw dataframes are NEVER stored in session state.
*   **Export State**: Handled statelessly using `st.download_button` which regenerates files on-click.

---

## SECTION 7 — CHART FRAMEWORK

A central factory module (`app/charts/chart_theme.py`) enforces strict visual compliance.

*   **Theme**: Injects the `#141414` background, hides Plotly's default grid lines, removes the legend (replaced by direct labels or title context).
*   **Typography**: Forces font to 'Inter', overriding Plotly defaults.
*   **Hover Templates**: Standardized format: `<br><b>%{x}</b><br>Metric: %{y:,.0f}`.
*   **Colors**: Primary data series uses high-luma Cyan (`#00E5FF`). Benchmark/Historical data uses Muted Grey (`#404040`). Critical highlights use Netflix Red (`#E50914`).
*   **Responsiveness**: `st.plotly_chart` always sets `use_container_width=True`.

---

## SECTION 8 — KPI ENGINE

A suite of pure Python functions calculates derived, defensible business metrics without faking financial data.

1.  **Catalog Freshness (%)**: (Titles added in the last 24 months) / (Total Titles).
2.  **Average Content Age (Years)**: Current Year - Release Year (Mean).
3.  **Series Survival Rate (%)**: (TV Shows with > 1 Season) / (Total TV Shows).
4.  **Genre Diversity Index**: Count of unique genres making up 80% of the catalog.
5.  **Mature Audience Share (%)**: (Titles rated TV-MA / R / NC-17) / (Total Titles).
6.  **Growth Velocity (YoY)**: Percentage change in titles added vs previous year.

*Validation*: Engine throws a `ValueError` if the input dataframe is missing required columns.

---

## SECTION 9 — PERFORMANCE STRATEGY

**Target**: < 1.5 second initial load; < 0.5 second filter refresh.

*   **Format**: Use Parquet over CSV for the processed data to reduce I/O time and preserve dtypes.
*   **Caching**: Core dataset loading function wrapped in `@st.cache_data`.
*   **Memory Management**: Drop raw string columns (like `description`) during the ETL phase before saving the `processed` dataframe, as they are not used in visualizations and bloat RAM.
*   **Lazy Evaluation**: Streamlit does not render charts inside unselected `st.tabs`. Place secondary charts inside tabs to defer rendering.

---

## SECTION 10 — ERROR HANDLING

*   **Missing Files**: Catch `FileNotFoundError` on startup. Display a full-screen `st.error` instructing the user to run the ETL pipeline (`make data`).
*   **Empty Datasets**: If a filter combination results in `len(df) == 0`, short-circuit the chart rendering loop and yield the `<EmptyState />` component.
*   **Invalid Filters**: If a user selects a Year where a chosen Genre did not exist, auto-reset the Genre filter to prevent a crash.
*   **Chart Failures**: Wrap `st.plotly_chart` calls in `try/except` blocks. If Plotly fails, render an `st.warning` instead of crashing the whole dashboard.

---

## SECTION 11 — TESTING STRATEGY

*   **Unit Tests (`tests/unit/`)**: `pytest` covering 100% of the KPI Engine and ETL string parsing (e.g., ensuring `duration` splitting correctly extracts seasons vs minutes).
*   **Data Validation (`tests/integration/`)**: Assertions ensuring the processed Parquet file has 0 unexpected nulls and correctly typed columns.
*   **UI Tests**: Basic structural tests using `pytest` to ensure Streamlit pages load without fatal exceptions.
*   **Coverage Target**: Minimum 80% line coverage for backend logic (excluding Streamlit UI components).

---

## SECTION 12 — CODE STANDARDS

*   **Style**: Strict PEP 8 enforced via `black` and `flake8`.
*   **Type Hints**: 100% type hinting required (`def get_kpi(df: pd.DataFrame) -> float:`). Validated by `mypy`.
*   **Docstrings**: Google-style docstrings for all business logic functions.
*   **Complexity**: Functions limited to 15 lines maximum. Cyclomatic complexity strictly under 5.
*   **Imports**: Absolute imports only (`from src.utils.formatting import ...`), sorted by `isort`.

---

## SECTION 13 — DEPLOYMENT ARCHITECTURE

*   **Local Development**: Managed via `Makefile`. `make install`, `make run`. Virtual environments required.
*   **Hosting**: Streamlit Community Cloud (for portfolio showcasing).
*   **Configuration**: Stored in `.streamlit/config.toml` for theme overrides (forcing dark mode).
*   **Secrets**: Handled via `.streamlit/secrets.toml` (ignored in git). Not actively required unless adding database connections later.

---

## SECTION 14 — RECRUITER EXPERIENCE (PORTFOLIO OPTIMIZATION)

The repo is designed for a 3-minute evaluation window.

1.  **README.md**:
    *   **Header**: High-quality GIF of the dashboard in action.
    *   **BLUF (Bottom Line Up Front)**: 3-sentence summary of the tech stack and the business problem solved.
    *   **Architecture Diagram**: A visual map of the ETL to Streamlit pipeline.
    *   **Live Link**: Prominent badge linking to the deployed Streamlit Cloud app.
2.  **Code Legibility**: Reviewers typically check `app/main.py` and one `tests/` file. These files must be perfectly documented and heavily commented.
3.  **Reproducibility**: Reviewers can run `pip install -r requirements.txt` and `streamlit run app/main.py` without requiring API keys, database setups, or complex Docker configurations.

---

## SECTION 15 — FINAL ENGINEERING CHECKLIST

*Tasks ordered strictly by implementation sequence.*

**Phase 1: Foundation (Data & Backend)**
1.  [ ] Initialize repo structure, virtual environment, and `requirements.txt`.
2.  [ ] Implement ETL logic (`src/data_pipeline/`) to output Parquet files.
3.  [ ] Implement KPI calculation engine (`src/kpi_engine/`).
4.  [ ] Write and pass unit tests for ETL and KPIs.

**Phase 2: App Shell (Frontend)**
5.  [ ] Configure `.streamlit/config.toml` (Dark Mode, Colors).
6.  [ ] Build `app/main.py` (Navigation, App Shell, Theme).
7.  [ ] Create blank multi-page files (`01_Dashboard.py`, etc.).
8.  [ ] Implement Data Loader with `@st.cache_data`.

**Phase 3: Components & State**
9.  [ ] Build `KPICard`, `InsightCard`, and `EmptyState` UI components.
10. [ ] Implement Sidebar/Top Global Filter drawer.
11. [ ] Wire filters to `st.session_state`.

**Phase 4: Chart Factory**
12. [ ] Define global Plotly layout theme (`app/charts/chart_theme.py`).
13. [ ] Build factory functions for standard charts (Bar, Area, Heatmap).
14. [ ] Standardize hover templates and formatting.

**Phase 5: Page Assembly**
15. [ ] Assemble Dashboard Landing Page.
16. [ ] Assemble Portfolio, Geography, and Genre deep-dive pages.
17. [ ] Integrate Insight & Recommendation text blocks.

**Phase 6: Polish & Launch**
18. [ ] Audit performance (load times < 2s).
19. [ ] Run final accessibility and contrast checks.
20. [ ] Write Recruiter-Optimized README.md and create GIF.
21. [ ] Deploy to Streamlit Community Cloud.
