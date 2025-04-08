import streamlit as st
from backend.auth import check_login, get_user_role
import importlib

st.set_page_config(page_title="Find Your Way Consulting Suite", page_icon="💼")

# Branding: logo and globe
st.markdown("""
<div style="text-align:center; margin-top: 10px;">
    <img src="https://i.gifer.com/7VE.gif" width="100"/>
</div>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login to Find Your Way Consulting Suite")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.authenticated = True
            st.session_state.user_role = get_user_role(username)
            st.success("Login successful!")
        else:
            st.error("Invalid login.")
else:
    role = st.session_state.user_role
    tab_map = {
        "📈 Forecasting": "forecasting",
        "📊 Sentiment": "sentiment_analysis",
        "🧠 Simulator": "strategic_simulator",
        "📝 Intake": "client_intake",
        "🎯 Positioning": "brand_positioning",
        "📊 KPI": "kpi_tracker",
        "📐 Strategy": "strategy_designer",
        "🧱 Canvas": "business_model_canvas",
        "⚙️ Ops Audit": "operations_audit",
        "🧲 Leads": "lead_generation",
        "📇 CRM": "crm_manager",
        "🌐 Network": "network_builder",
        "💼 Dev": "business_development",
        "🧠 Growth": "self_enhancement",
        "📢 Marketing": "marketing_hub",
        "💳 Credit Repair": "credit_repair"
    }

    tier_access = {
        "Basic": ["📈 Forecasting", "📊 Sentiment", "🧠 Simulator", "📝 Intake", "🎯 Positioning", "💳 Credit Repair"],
        "Elite": list(tab_map.keys())[:10] + ["💳 Credit Repair"],
        "Premium": list(tab_map.keys())[:-1] + ["💳 Credit Repair"],
        "Admin": list(tab_map.keys())
    }

    choice = st.selectbox("📊 Choose a tool", tier_access.get(role, []))
    folder = tab_map[choice]
    module = importlib.import_module(f"{folder}.{folder}_app")
    module.run()
