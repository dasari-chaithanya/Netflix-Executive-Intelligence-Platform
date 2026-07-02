# Changelog

All notable changes to the **Netflix Executive Intelligence Platform (NEIP)** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-02
### Added
- **Executive Overview**: Bloomberg-style alerting and 5-pillar health scorecard.
- **KPI Engine**: Decoupled module establishing single-source-of-truth formulas for Freshness, Diversity, and Expansion.
- **Analytics Engine**: Centralized data aggregation layer avoiding in-UI computation.
- **Strategy Sandbox**: Deterministic forecasting engine projecting metadata elasticity based on content investment scenarios.
- **Compare Mode**: Side-by-side regional catalog benchmarking.
- **MVC Architecture**: Implemented ViewModel layer to bridge UI and data layers, maximizing unit testability.
- **Parquet Store**: Upgraded ETL pipeline to output columnar `.parquet`, achieving sub-300ms query loads.
- **Recruiter Mode**: Toggleable portfolio presentation layer designed to surface architectural insights during technical interviews.

### Changed
- Rebranded entire platform to *Netflix Executive Intelligence Platform (NEIP)*.
- Purged all internal developer tools, debug screens, and layout inspectors to focus strictly on executive consumption.
- Deprecated static growth reports in favor of the interactive Insight Timeline.
