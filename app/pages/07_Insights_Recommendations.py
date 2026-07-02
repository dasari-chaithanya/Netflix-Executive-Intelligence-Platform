import streamlit as st
from app.components.layout import section_header, grid_row
from app.components.cards import insight_card, recommendation_card
from app.viewmodels.executive import ExecutiveViewModel

st.title("Insights & Recommendations")
st.markdown("Automated strategic takeaways based on current global filters.")

vm = ExecutiveViewModel()
data = vm.get_data()

section_header("Strategic Action Plan")

if data.get("is_empty"):
    st.info("No insights available for the current filter selection.")
else:
    # In a full implementation, we would iterate through a list of generated insights
    # For Milestone 3, we pull the single generated one from the ExecutiveViewModel
    col1, col2 = grid_row([1, 1])
    
    with col1:
        st.markdown("### Key Findings")
        insight = data["insight"]
        insight_card(insight["title"], insight["text"])
        
    with col2:
        st.markdown("### Recommended Actions")
        rec = data["recommendation"]
        recommendation_card(rec["title"], rec["action"])
