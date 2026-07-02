import streamlit as st
import plotly.graph_objects as go
import uuid

def story_card(title: str, value: str, delta: str = None, trend: str = "flat", 
               period: str = "Last 30 Days", chart_fig: go.Figure = None, 
               summary: str = None, recommendation: dict | str = None, 
               explanation: dict = None, badge: str = None):
    """
    Renders the unified "One Story" card that executives expect.
    """
    trend_color_map = {
        "up": "text-positive",
        "down": "text-negative",
        "flat": "text-secondary"
    }
    color_cls = trend_color_map.get(trend, "text-secondary")
    trend_arrow = "↑" if trend == "up" else "↓" if trend == "down" else "→"
    delta_str = f"{trend_arrow} {delta}" if delta else ""
    
    # Badge HTML
    badge_html = ""
    if badge:
        badge_color = "#22C55E" if badge.lower() in ["healthy", "excellent", "growing"] else "#FACC15" if badge.lower() in ["watch", "stable"] else "#EF4444"
        badge_html = f"<span style='background-color: {badge_color}20; color: {badge_color}; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: bold; margin-left: 8px;'>{badge}</span>"

    # Start Card
    st.markdown('<div class="story-card">', unsafe_allow_html=True)
    
    # KPI Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px;">
        <div>
            <div class="text-secondary" style="font-size: 0.95rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">{title} {badge_html}</div>
            <div style="font-size: 2.2rem; font-weight: 700; line-height: 1.2;">{value}</div>
        </div>
        <div style="text-align: right;">
            <div class="{color_cls}" style="font-size: 1.1rem; font-weight: 600;">{delta_str}</div>
            <div class="text-secondary" style="font-size: 0.8rem;">{period}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart
    if chart_fig:
        st.plotly_chart(chart_fig, use_container_width=True, config={'displayModeBar': False})
        
    # Storytelling / Recommendations
    if summary or recommendation:
        st.markdown("<hr style='border-top: 1px solid rgba(255,255,255,0.05); margin: 16px 0;'/>", unsafe_allow_html=True)
        if summary:
            st.markdown(f"<p style='font-size: 0.95rem; line-height: 1.5;'>{summary}</p>", unsafe_allow_html=True)
        if recommendation:
            if isinstance(recommendation, str):
                rec_html = f"<div style='font-size: 0.9rem;'>{recommendation}</div>"
            else:
                # Advanced dictionary recommendation
                rec_html = f"""
                <div style='font-size: 0.85rem; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;'>
                    <div><b>Priority:</b> <span style='color: #E50914;'>{recommendation.get('priority', 'HIGH')}</span></div>
                    <div><b>Impact:</b> {recommendation.get('impact', '★★★★☆')}</div>
                    <div><b>Reach:</b> {recommendation.get('reach', 'Global')}</div>
                    <div><b>Confidence:</b> {recommendation.get('confidence', 'High')}</div>
                </div>
                <div style='font-size: 0.9rem; margin-top: 8px;'><b>Action:</b> {recommendation.get('action', '')}</div>
                """
            st.markdown(f"""
            <div style="background: rgba(34, 197, 94, 0.1); border-left: 3px solid #22C55E; padding: 12px; border-radius: 4px; margin-top: 12px;">
                <div style="color: #22C55E; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Strategic Recommendation</div>
                {rec_html}
            </div>
            """, unsafe_allow_html=True)
            
    # Explain This Chart button (Rule-based)
    if explanation:
        with st.expander("💡 Explain Insight"):
            st.markdown(f"**Why this matters**: {explanation.get('why', 'Context not provided.')}")
            st.markdown(f"**Business impact**: {explanation.get('impact', 'Impact not provided.')}")
            st.markdown(f"**Opportunity**: {explanation.get('opportunity', 'None identified.')}")

    # End Card
    st.markdown('</div>', unsafe_allow_html=True)

# Keep the old cards for backwards compatibility if needed, but we will migrate pages to story_card.
def kpi_card(label: str, value: str, delta: str = None, trend: str = "flat", info: str = None):
    pass

def insight_card(title: str, text: str):
    pass

def recommendation_card(title: str, action: str):
    pass
