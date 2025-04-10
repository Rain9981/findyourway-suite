try:
    save_data(
        st.session_state.get("user_role", "guest"),
        {"input": user_input},
        sheet_tab="KPI Tracker"
    )
    st.info("✅ Data saved to Google Sheets.")
except Exception as e:
    if "already exists" in str(e):
        st.warning(f"✅ Sheet already exists, appending instead.")
    else:
        st.warning(f"Google Sheets not connected. Error: {e}")
