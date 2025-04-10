import streamlit as st

def run():
    st.title("🧭 Consulting Guide")

    st.sidebar.header("📘 Consulting Guide Info")
    st.sidebar.markdown("""
    - **Purpose:** This tab walks you through how to use each feature.
    - **What to do:** Review the strategic role of each tab.
    - **Access Level:** All users.
    """)

    st.markdown("## Consulting Walkthrough")
    st.markdown("""
    - **Brand Positioning:** Define your market identity.
    - **Lead Generation:** Get AI suggestions to attract new leads.
    - **CRM Dashboard:** Track and manage client data.
    - **Simulator:** Run scenarios and predict impact.
    - **Forecasting:** Project financial outcomes.
    """)
