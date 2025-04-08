import streamlit as st
import pandas as pd





def run():
    st.title("🧱 Business Model Canvas")
    st.markdown("### Define key elements of your model.")

    value_prop = st.text_input("Value Proposition")
    customer_segments = st.text_input("Customer Segments")

    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals())
        st.info("✅ Data saved to Google Sheets.")
    except:
        st.warning("Google Sheets not connected.")
