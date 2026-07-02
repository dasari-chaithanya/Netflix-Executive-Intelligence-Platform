import streamlit as st
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

st.set_page_config(page_title="Recommendations - Netflix Content Strategy", page_icon="🎯", layout="wide")
st.title("🎯 08: Actionable Recommendations")

insights_path = root_dir / 'insights.md'

if insights_path.exists():
    with open(insights_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "## Business Recommendations" in content:
        rec_section = content.split("## Business Recommendations")[1]
        st.markdown(rec_section)
    else:
        st.markdown(content)
else:
    st.info("Recommendations document not found. Run Notebook 05 to generate recommendations.")
