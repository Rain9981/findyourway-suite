import streamlit as st

def run():
    st.title("📊 CRM Dashboard")

    st.sidebar.header("💡 CRM Dashboard Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Displays upcoming client-facing CRM features.
    - **What to input:** No input needed yet.
    - **How to use:** Review upcoming feature notices or admin insights.
    """)

    st.info("🚧 This feature will soon display client engagement metrics and CRM dashboards.")
    st.markdown("""
        We are preparing:
        - Lead tracking dashboards
        - Client segmentation
        - KPI visualization
        - CRM syncing options
    """)
