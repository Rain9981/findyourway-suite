import streamlit as st
import importlib
import os

# ✅ Page Config – only once here
st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌟 Branding Section
st.markdown("""
<div style='text-align:center;'>
    <h1>🌍 Find Your Way Network Marketing Consultants</h1>
    <img src='https://raw.githubusercontent.com/Rain9981/findyourway-suite/main/assets/findyourway_logo.jpg' width='220' style='margin-top:15px;' alt='Find Your Way Logo'>
</div>
""", unsafe_allow_html=True)

# 🔐 Login Logic
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

# ✅ Ordered Tab Flow
tab_order = [
    "homepage",
    "client_intake",
    "subscription_plans",
    "consulting_guide",
    "brand_positioning",
    "business_development",
    "lead_generation",
    "marketing_hub",
    "strategy_designer",
    "business_model_canvas",
    "operations_audit",
    "self_enhancement",
    "growth",
    "kpi_tracker",
    "forecasting",
    "crm_manager",
    "crm_dashboard",
    "crm",  # CRM Insights
    "email_marketing",
    "credit_repair",
    "marketing_planner",
    "sentiment_analysis",
    "canvas",
    "oops_audit"
]

# Filter to only show existing tabs
available_tabs = [tab for tab in tab_order if os.path.isdir(tab) and os.path.exists(f"{tab}/{tab}_app.py")]

# Sidebar Tool Selector
selected = st.sidebar.selectbox("📂 Choose a Tool", available_tabs)

# ▶️ Load and Run Selected Tab
try:
    module = importlib.import_module(f"{selected}.{selected}_app")
    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"⚠️ Tab '{selected}' is missing a run() function.")
except Exception as e:
    st.error(f"🚨 Could not load tab: {e}")
