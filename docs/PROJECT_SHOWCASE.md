# Netflix Executive Intelligence Platform (NEIP) - Project Showcase

## Executive Summary
The Netflix Executive Intelligence Platform (NEIP) is a comprehensive Business Intelligence application designed for data-driven strategic planning. It transforms raw catalog metadata into actionable executive insights, enabling stakeholders to monitor content growth, evaluate regional catalog diversity, and simulate strategic investments.

## Business Problem
Netflix's catalog has expanded aggressively across international markets. Executives need a unified platform to answer critical questions:
- *Are we over-indexing on Movies versus TV Shows, risking long-term subscriber retention?*
- *Is our legacy catalog aging out faster than we can replenish it?*
- *Where should we allocate our next $100M regional production budget?*

Static dashboards fail to provide contextual decision support. NEIP solves this by offering dynamic, metadata-driven elasticity forecasting and centralized KPI monitoring.

## Architecture
NEIP follows a strict MVC (Model-View-Controller) architecture tailored for Streamlit:
- **Data Layer**: A PyArrow-backed Parquet columnar store.
- **Analytics & KPI Engine**: Pure Python modules that decouple business logic from the UI.
- **ViewModel Layer**: Serves formatted data to the frontend and handles aggressive caching.
- **UI Layer**: Reusable semantic components (Story Cards, Executive Scorecards).

## Core KPIs
- **Catalog Freshness**: Percentage of titles added in the last 24 months.
- **Average Content Age**: Mean IP age, acting as a proxy for retention risk.
- **Global Expansion Score**: Weighted index of non-US production volume and growth.
- **Diversity Score**: Geographic spread of content origins.

## Engineering Decisions & Trade-offs
*(See `DECISIONS.md` for a deep dive)*
- **Parquet over CSV**: Chosen for columnar compression and rapid read operations, reducing load times by over 80%.
- **Streamlit over React/Dash**: Prioritized rapid iteration and pure Python development to focus strictly on the backend Analytics Engine rather than managing complex frontend states.
- **Heuristics over Machine Learning**: The Strategy Sandbox intentionally avoids hallucinating ROI or subscriber metrics, instead using transparent metadata elasticity rules to project catalog diversity shifts.

## Business Impact
This platform enables executives to:
1. **Pivot Strategy**: Quickly identify whether the platform is leaning too heavily on volume acquisition vs. premium retention.
2. **Allocate Budgets**: Use the Market Expansion module to pinpoint under-indexed high-growth regions (e.g., South Korea, India).
3. **Forecast Diversity**: Use the Strategy Sandbox to simulate how a 15% increase in Anime production impacts overall catalog freshness and regional representation.

## Challenges Overcome
- **Memory Management**: Initial CSV loads were consuming excessive RAM. Migrating to Parquet and implementing `@st.cache_data` in the ViewModel layer resolved OOM issues and slashed render times.
- **UI Clutter**: Removed traditional grid lines, adopted a strict 5-color semantic palette, and abstracted complex metrics into high-level "Story Cards" to prevent cognitive overload.

## Future Scope
- Transition to a cloud data warehouse (Snowflake).
- Integration of an LLM for natural-language querying ("Ask the Platform").

## Interview Talking Points
- **Architecture**: Emphasize the separation of concerns (MVC) and how it enables easy migration to a cloud database without touching the UI.
- **Performance**: Discuss the I/O benefits of Parquet for analytical workloads.
- **Business Alignment**: Highlight that every chart exists to answer a specific business question, demonstrating product thinking over pure technical execution.
