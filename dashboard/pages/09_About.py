import streamlit as st

st.set_page_config(page_title="About - Netflix Content Strategy", page_icon="ℹ️", layout="wide")
st.title("ℹ️ 09: About the Project")

st.markdown("""
### Netflix Content Strategy Analysis
**An End-to-End Data Analytics Case Study**

This dashboard is the final product of an extensive data analytics case study examining Netflix's content catalog.

#### Key Features
* **Data Engineering**: A 9-step cleaning pipeline standardizing dates, missing values, and mixed formats.
* **Feature Engineering**: 12 derived features (e.g., `release_decade`, `movie_age`, `duration_category`).
* **Visual Analytics**: 35 professional visualizations answering 10 distinct business questions.
* **Insights**: 15 data-derived business insights.
* **Recommendations**: 9 actionable strategic recommendations based on the findings.

#### Technology Stack
* **Python**: Pandas, NumPy
* **Visualization**: Matplotlib, Seaborn, Plotly
* **Dashboard**: Streamlit
* **Documentation**: Markdown, ReportLab (PDFs)
* **Version Control**: Git / GitHub

#### Data Source
* **Dataset**: [Netflix Movies and TV Shows (Kaggle)](https://www.kaggle.com/datasets/shivamb/netflix-shows)
""")
