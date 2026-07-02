import streamlit as st
import plotly.graph_objects as go

def story_card(title: str, value: str, delta: str = None, trend: str = "flat", 
               period: str = "Last 30 Days", chart_fig: go.Figure = None, 
               summary: str = None, recommendation: dict | str = None, 
               explanation: dict = None, badge: str = None):
    """
    Renders the unified "One Story" card using Native Streamlit components.
    NO HTML is used to maintain a premium, unbreakable UI.
    """
    with st.container(border=True):
        # KPI Header
        badge_str = f" • [{badge}]" if badge else ""
        delta_color = "normal" if trend == "up" else "inverse" if trend == "down" else "off"
        # If trend is flat, delta color is off. Wait, if it's a good down (like churn), inverse is red.
        # But for generic, we'll map up to normal (green), down to inverse (red) or normal (green) depending.
        # Streamlit delta handles + as green and - as red by default.
        st.metric(label=f"{title}{badge_str}", value=value, delta=f"{delta} ({period})")
        
        # Chart
        if chart_fig:
            st.plotly_chart(chart_fig, use_container_width=True, config={'displayModeBar': False})
            
        # Storytelling / Recommendations
        if summary or recommendation:
            st.divider()
            if summary:
                st.markdown(summary)
            if recommendation:
                st.markdown("### Strategic Recommendation")
                if isinstance(recommendation, str):
                    st.markdown(recommendation)
                else:
                    priority = recommendation.get('priority', 'HIGH')
                    p_emoji = "🔴" if priority == 'HIGH' else "🟡" if priority == 'MEDIUM' else "🟢"
                    
                    st.markdown(f"**{p_emoji} {priority} PRIORITY**\n\n**{recommendation.get('impact', '★★★★☆')}** Impact\n\n**🌍 {recommendation.get('reach', 'Global')}** Reach\n\n**🎯 {recommendation.get('confidence', 'High')}** Confidence")
                    st.markdown(f"**Action**: {recommendation.get('action', '')}")
                
        # Explain This Chart button
        if explanation:
            with st.expander("💡 Explain Insight"):
                st.markdown(f"**Why this matters**: {explanation.get('why', 'Context not provided.')}")
                st.markdown(f"**Business impact**: {explanation.get('impact', 'Impact not provided.')}")
                if 'opportunity' in explanation:
                    st.markdown(f"**Opportunity**: {explanation.get('opportunity')}")

def executive_decision_closer(recommendation: str, impact: str, confidence: str, priority: str = "HIGH"):
    """
    Standard closer block to be appended to every page, shifting from insight to action.
    """
    st.divider()
    st.subheader("Executive Decision")
    
    col1, col2, col3 = st.columns(3)
    p_emoji = "🔴" if priority == 'HIGH' else "🟡" if priority == 'MEDIUM' else "🟢"
    
    with col1:
        st.metric("Priority", f"{p_emoji} {priority}")
    with col2:
        st.metric("Confidence", f"🎯 {confidence}")
    with col3:
        st.metric("Expected Impact", impact)
        
    st.success(f"**Recommendation**: {recommendation}")

def navigation_footer(next_page_name: str, next_page_path: str, next_page_desc: str, icon: str = "📈"):
    """
    Polished navigation footer to replace simple buttons.
    """
    st.divider()
    st.markdown(f"### Next Module")
    st.markdown(f"**{icon} {next_page_name}**")
    st.markdown(next_page_desc)
    st.page_link(next_page_path, label=f"Open {next_page_name} →", icon="👉")
