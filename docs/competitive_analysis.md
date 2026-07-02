# Competitive Dashboard Analysis

To ensure the Netflix Content Strategy Platform meets enterprise standards, it was benchmarked against top-tier public dashboards from the Tableau Public Gallery and Power BI Data Stories Gallery.

## 1. Tableau Public (Featured Dashboards)
**Observation**: The best Tableau dashboards prioritize narrative over raw chart count. They use text boxes to explain *why* the data matters.
**Implementation**: This project adopts the **Storytelling Layer** (`app/business/storytelling.py`). Every chart is paired with a dynamically generated "Insight Card" and "Recommendation Card" that explains the business impact of the visual.

## 2. Power BI Data Stories Gallery
**Observation**: Power BI heavily utilizes a persistent, left-aligned filter pane that affects all subsequent tabs (cross-filtering).
**Implementation**: We implemented a global `st.sidebar` filter panel. The state is managed via `st.session_state` and applied to the `BaseViewModel`, meaning users do not need to re-filter data when navigating between the "Content Analytics" and "Global Expansion" pages.

## 3. Standard Streamlit Gallery
**Observation**: Many Streamlit apps feel like "scripts" rather than "products." They expose raw dataframes, dump tracebacks on error, and lack a cohesive grid.
**Implementation**: This project introduces a UI Component framework (`app/components/`) to wrap Streamlit primitives. The result is a dashboard that looks and feels like a bespoke React application, complete with a strict token-based CSS theme generator.

## Verdict
By combining Tableau's narrative focus, Power BI's global state management, and Streamlit's rapid prototyping speed, this platform stands as a highly competitive, production-ready enterprise tool.
