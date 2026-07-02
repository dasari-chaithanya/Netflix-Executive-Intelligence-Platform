<div align="center">
  <img src="docs/assets/hero_banner.png" alt="Netflix Executive Intelligence Platform" width="100%" />

  # Netflix Executive Intelligence Platform

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
  [![Pandas](https://img.shields.io/badge/Pandas-2.2.0-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

<br>

<div align="center">
  <img src="docs/assets/demo/demo_placeholder.gif" alt="Platform Demo" width="800px" />
  <p><i>The Executive Intelligence Platform in action.</i></p>
</div>

---

## 📌 Project Overview
The **Netflix Executive Intelligence Platform** is a production-grade, full-stack Business Intelligence application. It replaces static dashboards with a dynamic, metadata-driven decision-making engine. Built to answer specific strategic questions regarding content pacing, global market expansion, and audience retention, the platform strictly follows a Model-View-Controller (MVC) architecture optimized for executive consumption.

## 💼 Business Value
This platform supports high-level executive decisions by providing factual, data-driven insights into the Netflix catalog:
- Monitor **Catalog Growth** and shifting investment from Movies to Premium TV Originals.
- Identify **Market Expansion** opportunities and allocate regional production budgets.
- Evaluate **Content Freshness** and calculate long-term retention risks.
- Compare regional catalogs via **Side-by-Side Market Analysis**.
- Support strategic planning using the **Strategy Sandbox** to simulate catalog elasticity based on historic metadata.

## 🏗️ Architecture

```mermaid
graph TD
    A[Raw Dataset] -->|ETL Pipeline| B(Parquet Store)
    B --> C{Analytics Engine}
    C --> D[KPI Engine]
    D --> E[ViewModels]
    E -->|Streamlit UI| F[Executive Dashboards]
    E -->|Streamlit UI| G[Strategy Sandbox]
```

## 🧩 Core Modules

| Module | Business Question |
|--------|-------------------|
| **Executive Overview** | What is the high-level health of our global content library today? |
| **Growth Intelligence** | Has our content strategy shifted from volume acquisition to premium originals? |
| **Market Expansion** | Where should Netflix allocate its next regional production budget? |
| **Content Portfolio** | What is the structural composition and rating focus of our global catalog? |
| **Audience Strategy** | Which genres and formats drive the highest long-term viewer retention? |
| **Compare Markets** | How do content strategies differ between distinct geographic regions? |
| **Strategy Sandbox** | How do targeted content investments impact catalog diversity and freshness? |

## 📸 Screenshots

<details>
<summary><b>1. Executive Overview</b></summary>
<br>
<img src="docs/assets/screenshots/executive_overview_placeholder.png" alt="Executive Overview" width="800px">
<i>Provides immediate strategic alerts and a 5-pillar health scorecard.</i>
</details>

<details>
<summary><b>2. Market Expansion</b></summary>
<br>
<img src="docs/assets/screenshots/market_expansion_placeholder.png" alt="Market Expansion" width="800px">
<i>Identifies production hotspots globally.</i>
</details>

<details>
<summary><b>3. Strategy Sandbox</b></summary>
<br>
<img src="docs/assets/screenshots/strategy_sandbox_placeholder.png" alt="Strategy Sandbox" width="800px">
<i>Calculates the impact of hypothetical investments on diversity and freshness.</i>
</details>

## 📂 Folder Structure

```text
Netflix-Executive-Intelligence-Platform/
├── app/
│   ├── components/       # Reusable UI elements (Story Cards, Filters)
│   ├── pages/            # Streamlit dashboard views
│   ├── state/            # Session state and cache management
│   ├── theme/            # CSS tokens and styling injection
│   └── main.py           # Application entry point and sidebar navigation
├── docs/                 # Architecture, Screenshots, and Assets
├── src/
│   ├── analytics_engine/ # Complex aggregation logic
│   ├── config/           # Centralized configuration and design tokens
│   ├── data_pipeline/    # ETL scripts (Cleaning, Feature Engineering)
│   └── kpi_engine/       # Standardized business metric formulas
├── tests/                # Pytest suite (Unit, Integration, UI)
├── README.md             
├── requirements.txt      
└── LICENSE               
```

## 🚀 Installation & Deployment

### Local Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/Netflix-Executive-Intelligence-Platform.git
cd Netflix-Executive-Intelligence-Platform
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the ETL pipeline (Optional, Parquet files are included):
```bash
python src/data_pipeline/etl.py
```
4. Launch the application:
```bash
streamlit run app/main.py
```

## 📄 Resume Highlights
- **Architected** a Netflix Catalog Intelligence platform using Python, Streamlit, and PyArrow, reducing data load times to `<300ms` via Parquet columnar caching.
- **Engineered** an MVC-patterned application separating the UI layer from a highly tested KPI Engine and Analytics Engine.
- **Designed** a "Strategy Sandbox" feature to calculate metadata elasticity and forecast catalog diversity shifts based on simulated production investments.
- **Implemented** a responsive, executive-focused UX design utilizing strict semantic design tokens, Bloomberg-style strategic alerts, and dynamic rule-based text generation.

## 🎯 Interview Preparation (Talking Points)
- **Why Parquet?** "Parquet is a columnar format. Since analytics dashboards usually query specific columns rather than entire rows, Parquet drastically reduces memory overhead and I/O wait times compared to CSV."
- **Why Streamlit?** "Streamlit allows rapid iteration of the presentation layer in pure Python, enabling me to focus my engineering efforts on the backend Analytics Engine rather than managing React state."
- **Why the ViewModel layer?** "It decouples the UI from the data. If the underlying database changes from a Parquet file to Snowflake or BigQuery, the UI code doesn't need a single modification."
- **How did you handle performance?** "I utilized `@st.cache_data` on the ViewModels to prevent re-querying the data pipeline on every UI interaction, guaranteeing near-instant rendering."

## 🔮 Future Scope
- Integration with an LLM (e.g. GPT-4) to power natural language querying for the "Ask the Platform" feature.
- Migrate the backend Parquet data store to a cloud data warehouse (Snowflake / BigQuery).
- Introduce a secure authentication layer via OAuth2.

## 🤝 Connect
- **LinkedIn:** [Your LinkedIn Profile URL]
- **Portfolio:** [Your Portfolio Website URL]
- **Email:** [Your Email Address]
