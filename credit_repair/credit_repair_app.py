import streamlit as st

def run():
    st.title("💳 Credit Repair Portal")

    st.sidebar.header("💡 Credit Repair Info")
    st.sidebar.markdown("""
    - **What this tab does:** Connects users to the credit repair SaaS system.
    - **Access:** Elite + Premium users only.
    - **Tip:** Direct clients to [your credit site](https://findyourwaynmc.creditmyreport.com).
    """)

    st.markdown("### Start Your Credit Journey")
    st.markdown("Click below to access your credit repair tools.")
    st.link_button("Go to Credit Repair Platform", "https://findyourwaynmc.creditmyreport.com")
