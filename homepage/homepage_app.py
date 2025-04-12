import streamlit as st

def run():
    st.set_page_config(page_title="Welcome | Find Your Way Suite", layout="centered")

    st.title("🌐 Welcome to Find Your Way AI Consulting Suite")

    st.sidebar.header("🧭 Getting Started")
    st.sidebar.markdown("""
    - Begin with **Client Intake**  
    - Use tabs based on your tier  
    - Save/export via Sheets or PDF  
    - Need help? Click contact button below
    """)

    # 👤 Greet by tier
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

    # 🌍 Animated Business Visual
    st.image("https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif", width=400, caption="Find Your Way Forward ✨")

    # ✅ Quick Help Buttons
    col1, col2, col3 = st.columns(3
