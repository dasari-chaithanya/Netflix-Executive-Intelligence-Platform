# Contributing to the Netflix Executive Intelligence Platform

First off, thank you for considering contributing to this project!

## Development Environment Setup

1. Fork and clone the repository.
2. Create a virtual environment (`python -m venv venv`).
3. Install the requirements (`pip install -r requirements.txt`).
4. Run the tests (`pytest`) to ensure your base is clean.

## Pull Request Process

1. **Keep it focused:** Ensure your PR addresses a single issue or adds a specific feature.
2. **Follow the Architecture:** 
   - Never perform data aggregation or calculation inside `app/pages/*.py`.
   - Business logic belongs in `src/analytics_engine/` or `src/kpi_engine/`.
   - Data passing to the UI must go through `app/viewmodels/`.
3. **Tests Required:** Any new KPI or analytical function must have a corresponding test in `tests/unit/`.
4. **Update Documentation:** If you add a new metric, define it in `app/pages/08_Business_Glossary.py`.

## Code Style

- Use type hints wherever possible.
- Adhere to PEP 8 standards.
- Run `pytest` before submitting to ensure no existing logic is broken.
