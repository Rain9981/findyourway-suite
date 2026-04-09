import streamlit as st
import importlib
import os
from backend.auth_manager import authenticate_user

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌟 Logo
st.image(
    "https://raw.githubusercontent.com/Rain9981/findyourway-suite/main/assets/logo2Find_You_Way_v2.png",
    width=220,
    caption=None,
)

# 🔐 Login State Init
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = "guest"

# 🔐 LOGIN SYSTEM (UPDATED — SAFE VERSION)
if not st.session_state["logged_in"]:
    st.title("🔐 Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        username_clean = username.strip().lower()
        password_clean = password.strip()

        # ✅ 1. Try Google Sheets users FIRST
        success, role = authenticate_user(username_clean, password_clean)

        if success:
            st.session_state["user_role"] = role

        # ✅ 2. FALLBACK (your current system — unchanged logic)
        elif username_clean == "admin" and password_clean == "FindYourWayNMC520":
            st.session_state["user_role"] = "admin"

        elif username_clean == "premium" and password_clean == "premium":
            st.session_state["user_role"] = "premium"

        elif username_clean == "elite" and password_clean == "elite":
            st.session_state["user_role"] = "elite"

        elif username_clean == "basic" and password_clean == "basic":
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
    "basic": [
        "homepage",
        "subscription_plans",
        "consulting_guide",
        "brand_positioning",
        "strategy_designer",
        "network_builder",
        "future_self_deep_state",
        "credit_repair"
    ],

    "elite": [
        "homepage",
        "subscription_plans",
        "consulting_guide",
        "brand_positioning",
        "business_development",
        "strategy_designer",
        "lead_generation",
        "network_builder",
        "marketing_hub",
        "operations_audit",
        "future_self_deep_state",
        "growth",
        "kpi_tracker",
        "forecasting",
        "credit_repair"
    ],

    "premium": [
        "homepage",
        "subscription_plans",
        "consulting_guide",
        "brand_positioning",
        "business_development",
        "strategy_designer",
        "lead_generation",
        "network_builder",
        "marketing_hub",
        "marketing_planner",
        "email_marketing",
        "sentiment_analysis",
        "operations_audit",
        "oops_audit",
        "future_self_deep_state",
        "growth",
        "kpi_tracker",
        "forecasting",
        "canvas",
        "credit_repair"
    ],

    "admin": [
        "homepage",
        "subscription_plans",
        "consulting_guide",
        "client_intake",
        "brand_positioning",
        "business_development",
        "strategy_designer",
        "business_model_canvas",
        "business_genius_engine",
        "lead_generation",
        "network_builder",
        "marketing_hub",
        "marketing_planner",
        "email_marketing",
        "sentiment_analysis",
        "mastermind_analyzer",
        "operations_audit",
        "oops_audit",
        "self_enhancement",
        "future_self_deep_state",
        "growth",
        "kpi_tracker",
        "forecasting",
        "credit_repair",
        "canvas",
        "crm_manager",
        "crm",
        "crm_dashboard",

        # 🔥 keep admin tool
        "admin_user_manager"
    ]
}
# ✅ Tab Visibility Logic
tab_order = [
    "homepage",
    "subscription_plans",
    "consulting_guide",
    "client_intake",

    "brand_positioning",
    "business_development",
    "strategy_designer",
    "business_model_canvas",
    "business_genius_engine",

    "lead_generation",
    "network_builder",
    "marketing_hub",
    "marketing_planner",
    "email_marketing",
    "sentiment_analysis",
    "mastermind_analyzer",

    "operations_audit",
    "oops_audit",

    "self_enhancement",
    "future_self_deep_state",
    "growth",
    "kpi_tracker",
    "forecasting",

    "credit_repair",
    "canvas",

    # CRM FLOW (admin only)
    "crm_manager",
    "crm",
    "crm_dashboard",

    # 🔥 keep admin tool visible
    "admin_user_manager"
]
allowed_tabs = tier_access.get(role, [])

available_tabs = [
    tab for tab in tab_order
    if tab in allowed_tabs
    and os.path.isdir(tab)
    and os.path.exists(f"{tab}/{tab}_app.py")
]

# 🔍 Debug Import Check
tab_modules = {}

for tab in available_tabs:
    try:
        mod = importlib.import_module(f"{tab}.{tab}_app")
        tab_modules[tab] = mod
        print(f"✅ Loaded tab: {tab}")
    except Exception as e:
        print(f"❌ Failed to import tab: {tab} — {e}")

selected = st.sidebar.selectbox("📂 Choose a Tool", available_tabs)

# ▶️ Load Selected Tab
try:
    if selected not in allowed_tabs:
        st.warning("🔒 This tool is not available on your current subscription.")
    else:
        module = importlib.import_module(f"{selected}.{selected}_app")
        if hasattr(module, "run"):
            module.run()
        else:
            st.error(f"⚠️ Tab '{selected}' is missing a run() function.")
except Exception as e:
    st.error(f"🚨 Could not load tab: {e}")