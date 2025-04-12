import streamlit as st
import importlib
import os

# ✅ Page Setup
st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌍 Header: Title + Subtitle + Globe
st.markdown("""
<div style='text-align:center; padding-bottom:20px;'>
    <h1 style='color:#800020; font-size: 40px; font-weight: bold; margin-bottom: 5px;'>Find Your Way</h1>

    <p style='font-size:18px; color:#000000; font-weight:300; margin-top:0;'>Network Marketing Consultants</p>

    <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Blue_Marble_2001.png/300px-Blue_Marble_2001.png'
         width='60' alt='Globe' style='margin-top:10px;' />
</div>
""", unsafe_allow_html=True)

# 🔐 Login Setup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = "guest"

if not st.session_state["logged_in"]:
    st.title("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == "FindYourWayNMC520":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "admin"
            st.rerun()
        elif password == "premium":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "premium"
            st.rerun()
        elif password == "elite":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "elite"
            st.rerun()
        elif password == "basic":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "basic"
            st.rerun()
        else:
            st.error("Invalid login")
    st.stop()

# ✅ Sidebar: Show Role
st.sidebar.markdown(f"🧾 **Logged in as:** `{st.session_state['user_role'].capitalize()}`")

# ✅ Tab Navigation
tab_order = [
    "homepage", "client_intake", "subscription_plans", "consulting_guide",
    "brand_positioning", "business_development", "lead_generation", "marketing_hub",
    "strategy_designer", "business_model_canvas", "operations_audit", "self_enhancement",
    "growth", "kpi_tracker", "forecasting", "crm_manager", "crm_dashboard", "crm",
    "email_marketing", "credit_repair", "marketing_planner", "sentiment_analysis",
    "canvas", "oops_audit"
]

available_tabs = [tab for tab in tab_order if os.path.isdir(tab) and os.path.exists(f"{tab}/{tab}_app.py")]
selected = st.sidebar.selectbox("📂 Choose a Tool", available_tabs)

# ▶️ Load Selected Tab
try:
    module = importlib.import_module(f"{selected}.{selected}_app")
    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"⚠️ Tab '{selected}' is missing a run() function.")
except Exception as e:
    st.error(f"🚨 Could not load tab: {e}")
