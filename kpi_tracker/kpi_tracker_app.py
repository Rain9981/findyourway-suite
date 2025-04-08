import streamlit as st
import pandas as pd





def run():
    st.title("📊 KPI Tracker")
    st.markdown("### Track key performance indicators.")

    kpi_name = st.text_input("KPI Name")
    kpi_value = st.number_input("Current Value", min_value=0, value=0, step=1)

    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals())
        st.info("✅ Data saved to Google Sheets.")
    except:
        st.warning("Google Sheets not connected.")
