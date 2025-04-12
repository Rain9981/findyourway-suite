import streamlit as st
import datetime

def run():
    st.title("🌐 Welcome to Find Your Way AI Consulting Suite")

    st.sidebar.header("🧭 Getting Started")
    st.sidebar.markdown("""
    - Begin with **Client Intake**  
    - Use tabs based on your tier  
    - Save/export via Sheets or PDF  
    - Need help? Click contact button below
    """)

    role = st.session_state.get("user_role", "guest")
    if role == "admin":
        greeting = "Welcome, Admin! You have full access to all tools and exports."
    elif role == "premium":
        greeting = "Welcome, Premium Member! Dive deep into strategy, CRM, and growth tools."
    elif role == "elite":
        greeting = "Welcome, Elite Client! Explore advanced planning and lead generation."
    elif role == "basic":
        greeting = "Welcome, Basic User! Start with client intake and forecasting tools."
    else:
        greeting = "Welcome! Please log in to access your consulting tools."

    st.subheader(greeting)

    st.image("https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif", width=400, caption="Find Your Way Forward ✨")

    st.markdown("### 🔗 Quick Navigation")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Client Intake"):
            st.info("Go to the 'Client Intake' tab above.")
    with col2:
        if st.button("📘 Walkthrough Guide"):
            st.info("Visit the 'Consulting Guide' tab for tips.")
    with col3:
        if st.button("📊 CRM Dashboard"):
            st.info("Access the CRM Dashboard tab above.")

    st.divider()

    if st.button("📨 Contact Support"):
        st.markdown("Please email us at [support@findyourwaynmc.com](mailto:support@findyourwaynmc.com)")
