# Future Enhancements Roadmap

The **Netflix Executive Intelligence Platform (NEIP)** is designed to scale. This roadmap outlines the technology-focused evolution of the platform.

### Phase 1: Data Infrastructure Modernization
- **Cloud Data Warehouse Integration**: Migrate the local Parquet backend to **Snowflake** or **Google BigQuery** to handle real-time streaming data ingestion.
- **dbt (Data Build Tool)**: Replace the custom python `data_pipeline/etl.py` with dbt models to standardize transformations and integrate automated data quality tests.

### Phase 2: Advanced Analytics & AI
- **LLM-Powered Natural Language Queries**: Integrate an open-source LLM (e.g., Llama 3) to allow executives to type questions like *"Show me the fastest growing genre in APAC"* and dynamically generate SQL or dataframe filters.
- **Recommendation Engine Integration**: Incorporate collaborative filtering outputs (if subscriber data becomes available) to map content acquisition directly to user retention cohorts.

### Phase 3: Platform Extensibility
- **Automated PDF/Email Reporting**: Implement a backend cron job utilizing `ReportLab` to snapshot the dashboard state and email a weekly "Executive Mission Brief" to stakeholders.
- **Authentication & RBAC**: Implement OAuth2 and Role-Based Access Control so Regional Managers only see data relevant to their specific territories.
- **Power BI / Tableau Connectors**: Expose the `Analytics Engine` via a FastAPI semantic layer, allowing external enterprise BI tools to securely consume the cleaned Netflix metrics.
