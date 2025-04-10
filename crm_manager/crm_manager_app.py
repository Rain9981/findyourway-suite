import streamlit as st

def run():
    st.title("🧠 CRM Manager")

    st.sidebar.header("💡 CRM Manager Insights")
    st.sidebar.markdown("""
    - **Purpose:** For admin/client managers to oversee CRM records.
    - **Access:** Admin only
    - **Tip:** Use this to verify team usage and exports.
    """)

    st.success("Admin view active. CRM export + sync tools coming soon.")
