# Engineering & Architectural Decisions

This document outlines the major technical decisions, trade-offs, and design rationale behind the **Netflix Executive Intelligence Platform (NEIP)**.

## 1. Parquet over CSV for Data Storage
**Decision**: The ETL pipeline converts the raw dataset into a `.parquet` file for the application to consume, rather than querying the raw `.csv`.
**Rationale**: Parquet is a columnar storage format. Analytics dashboards typically aggregate specific columns (e.g., `release_year`, `type`) across millions of rows. Parquet reads only the required columns, drastically reducing I/O wait times and memory overhead.
**Trade-off**: Requires an upfront ETL transformation step, but the resulting `<300ms` UI load time justifies the pipeline overhead.

## 2. Streamlit for the Presentation Layer
**Decision**: Built the frontend using Streamlit instead of Dash or a custom React application.
**Rationale**: Streamlit allows for rapid iteration of data products in pure Python. Given the project focus on Data Analytics and BI, time was better spent hardening the backend `Analytics Engine` and `KPI Engine` rather than managing Javascript state or API endpoints.
**Trade-off**: Streamlit's execution model (running top-to-bottom on every interaction) requires strict caching strategies to maintain performance.

## 3. Strict MVC Architecture
**Decision**: Decoupled the UI from the business logic using a ViewModel pattern.
**Rationale**: `app/pages/*.py` files contain zero data manipulation. They only import `app/viewmodels/`, which handle caching and format the outputs of `src/analytics_engine/`. 
**Trade-off**: Increased boilerplate code and file structure complexity, but guarantees that the application is unit-testable and database-agnostic.

## 4. Heuristics over Machine Learning in the Strategy Sandbox
**Decision**: The Strategy Sandbox calculates "Expected Impact" on diversity and freshness using static elasticity rules rather than predictive ML models.
**Rationale**: The dataset lacks financial, viewership, or subscriber data. Attempting to predict "ROI" or "Revenue" would require hallucinating data, which destroys analytical credibility in an executive setting. Transparent heuristics based purely on existing metadata maintain absolute defensibility.
**Trade-off**: Limits the "wow factor" of predictive AI, but significantly increases trust and engineering maturity.

## 5. Semantic Design Tokens
**Decision**: Centralized all styling in `src/config/design_tokens.json`.
**Rationale**: Hardcoding colors in Plotly or Streamlit creates technical debt. Using design tokens ensures that the Netflix branding (Red/Black/White) and semantic indicators (Green for Growth, Yellow for Watch) remain perfectly consistent across the entire platform.
