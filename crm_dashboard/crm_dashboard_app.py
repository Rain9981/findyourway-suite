import streamlit as st

def run():
    st.title("📊 CRM Dashboard")

    st.sidebar.header("💡 Dashboard Info")
    st.sidebar.markdown("""
    - **What this tab does:** Summarizes CRM activity and performance.
    - **What's coming:** Filtered views, KPI summaries, live charts.
    - **Tip:** Export reports directly from the dashboard (Admin only).
    """)

    st.info("🚧 This feature will soon display client engagement metrics and charts.")
