import streamlit as st
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

st.set_page_config(page_title="Insights - Netflix Content Strategy", page_icon="💡", layout="wide")
st.title("💡 07: Business Insights")

insights_path = root_dir / 'insights.md'

if insights_path.exists():
    with open(insights_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract only the insights section
    if "## Business Insights" in content and "## Business Recommendations" in content:
        insights_section = content.split("## Business Insights")[1].split("## Business Recommendations")[0]
        st.markdown(insights_section)
    else:
        st.markdown(content)
else:
    st.info("Insights document not found. Run Notebook 05 to generate insights.")
