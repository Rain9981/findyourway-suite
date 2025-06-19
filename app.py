import streamlit as st
import importlib
import os

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌟 Logo
st.image(
    "https://raw.githubusercontent.com/Rain9981/findyourway-suite/main/assets/logo2Find_You_Way_v2.png",
    width=220,
    caption=None,
)

# 🔐 Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = "guest"

if not st.session_state["logged_in"]:
    st.title("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == "FindYourWayNMC520":
            st.session_state["user_role"] = "admin"
        elif password == "premium":
            st.session_state["user_role"] = "premium"
        elif password == "elite":
            st.session_state["user_role"] = "elite"
        elif password == "basic":
            st.session_state["user_role"] = "basic"
        else:
            st.error("Invalid login")
            st.stop()
        st.session_state["logged_in"] = True
        st.rerun()

# ✅ Sidebar: Role Display
role = st.session_state.get("user_role", "guest")
st.sidebar.markdown(f"🧾 **Logged in as:** `{role.capitalize()}`")

# ✅ Tier Access Dictionary
tier_access = {
    "basic": ["homepage", "client_intake", "subscription_plans", "consulting_guide", "credit_repair"],
    "elite": [
        "homepage", "client_intake", "subscription_plans", "consulting_guide",
        "brand_positioning", "business_development", "lead_generation", "marketing_hub",
        "strategy_designer", "operations_audit", "growth", "kpi_tracker", "forecasting", "credit_repair"
    ],
    "premium": [
        "homepage", "client_intake", "subscription_plans", "consulting_guide",
        "brand_positioning", "business_development", "lead_generation", "marketing_hub",
        "strategy_designer", "operations_audit", "growth", "kpi_tracker", "forecasting",
        "crm_manager", "crm_dashboard", "crm", "email_marketing", "credit_repair",
        "marketing_planner", "sentiment_analysis", "canvas", "oops_audit"
    ],
    "admin": [  # Full access
        "homepage", "client_intake", "subscription_plans", "consulting_guide",
        "brand_positioning", "business_development", "lead_generation", "marketing_hub",
        "strategy_designer", "business_model_canvas", "operations_audit", "self_enhancement",
        "growth", "kpi_tracker", "forecasting", "crm_manager", "crm_dashboard", "crm",
        "email_marketing", "credit_repair", "marketing_planner", "sentiment_analysis",
        "canvas", "oops_audit", "business_genius_engine", "mastermind Analyzer"
    ]
}

# ✅ Tab Visibility Logic
tab_order = [
    "homepage", "client_intake", "subscription_plans", "consulting_guide",
    "brand_positioning", "business_development", "lead_generation", "marketing_hub",
    "strategy_designer", "business_model_canvas", "operations_audit", "self_enhancement",
    "growth", "kpi_tracker", "forecasting", "crm_manager", "crm_dashboard", "crm",
    "email_marketing", "credit_repair", "marketing_planner", "sentiment_analysis",
    "canvas", "oops_audit", "business_genius_engine", "Mastermind Analyzer"
]

allowed_tabs = tier_access.get(role, [])
available_tabs = [tab for tab in tab_order if tab in allowed_tabs and os.path.isdir(tab) and os.path.exists(f"{tab}/{tab}_app.py")]

selected = st.sidebar.selectbox("📂 Choose a Tool", available_tabs)

# ▶️ Load Selected Tab with Try Block
try:
    if selected not in allowed_tabs:
        st.warning("🔒 This tool is not available on your current subscription. Upgrade to unlock it.")
    else:
        module = importlib.import_module(f"{selected}.{selected}_app")
        if hasattr(module, "run"):
            module.run()
        else:
            st.error(f"⚠️ Tab '{selected}' is missing a run() function.")
except Exception as e:
    st.error(f"🚨 Could not load tab: {e}")
