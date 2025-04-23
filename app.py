import streamlit as st
import importlib
import os

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌟 Logo + Header
st.image(
    "https://raw.githubusercontent.com/Rain9981/findyourway-suite/main/assets/logo2Find_You_Way_v2.png",
    width=220,
    caption=None,
)



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

# ✅ Sidebar: Role Indicator
st.sidebar.markdown(f"🧾 **Logged in as:** `{st.session_state['user_role'].capitalize()}`")

# ✅ Ordered Tabs
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

# ▶️ Load Selected Tool
try:
    module = importlib.import_module(f"{selected}.{selected}_app")
    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"⚠️ Tab '{selected}' is missing a run() function.")
except Exception as e:
    st.error(f"🚨 Could not load tab: {e}")
