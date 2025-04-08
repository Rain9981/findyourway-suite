import streamlit as st
import pandas as pd





def run():
    st.title("📝 Client Intake Form")
    st.markdown("### Collect client onboarding info.")

    client_name = st.text_input("Client Name")
    industry = st.text_input("Industry")
    goals = st.text_area("Client Goals")

    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals())
        st.info("✅ Data saved to Google Sheets.")
    except:
        st.warning("Google Sheets not connected.")
