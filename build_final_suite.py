import os

def write_file(path, content):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# -----------------------
# Main Streamlit app.py
# -----------------------
app_py = '''import streamlit as st
from backend.auth import check_login, get_user_role
import importlib

st.set_page_config(page_title="Find Your Way Consulting Suite", page_icon="💼")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.markdown('<div style="text-align:center;"><img src="https://i.gifer.com/7VE.gif" width="100"/></div>', unsafe_allow_html=True)

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
        "Basic": ["📈 Forecasting", "📊 Sentiment", "🧠 Simulator", "📝 Intake", "🎯 Positioning"],
        "Elite": ["📈 Forecasting", "📊 Sentiment", "🧠 Simulator", "📝 Intake", "🎯 Positioning", "📊 KPI", "📐 Strategy", "🧱 Canvas", "⚙️ Ops Audit"],
        "Premium": ["📈 Forecasting", "📊 Sentiment", "🧠 Simulator", "📝 Intake", "🎯 Positioning", "📊 KPI", "📐 Strategy", "🧱 Canvas", "⚙️ Ops Audit", "🧲 Leads", "📇 CRM", "🌐 Network"],
        "Admin": list(tab_map.keys())
    }

    choice = st.selectbox("📊 Choose a tool", tier_access.get(role, []))
    folder = tab_map[choice]
    module = importlib.import_module(f"{folder}.{folder}_app")
    module.run()
'''

# -------------------------
# backend/auth.py logic
# -------------------------
auth_py = '''def check_login(username, password):
    users = {
        "basic": {"password": "basic123", "role": "Basic"},
        "elite": {"password": "elite123", "role": "Elite"},
        "premium": {"password": "premium123", "role": "Premium"},
        "admin": {"password": "FindYourWayNMC520", "role": "Admin"}
    }
    return username in users and users[username]["password"] == password

def get_user_role(username):
    return {
        "basic": "Basic",
        "elite": "Elite",
        "premium": "Premium",
        "admin": "Admin"
    }[username]
'''

# -------------------------
# Tab folders + placeholders
# -------------------------
tabs = [
    ("forecasting", "📈 Forecasting", "Business forecast simulator"),
    ("sentiment_analysis", "📊 Sentiment", "Market sentiment analysis"),
    ("strategic_simulator", "🧠 Simulator", "Strategy decision simulation"),
    ("client_intake", "📝 Intake", "New client intake form"),
    ("brand_positioning", "🎯 Positioning", "Brand clarity & messaging"),
    ("kpi_tracker", "📊 KPI", "Track and measure key metrics"),
    ("strategy_designer", "📐 Strategy", "Build and export strategic plans"),
    ("business_model_canvas", "🧱 Canvas", "Business model blueprint"),
    ("operations_audit", "⚙️ Ops Audit", "Internal systems review"),
    ("lead_generation", "🧲 Leads", "Lead capture & nurturing"),
    ("crm_manager", "📇 CRM", "Full CRM input + client database"),
    ("network_builder", "🌐 Network", "Build referral/partner map"),
    ("business_development", "💼 Dev", "Growth planning templates"),
    ("self_enhancement", "🧠 Growth", "Owner/founder enhancement"),
    ("marketing_hub", "📢 Marketing", "Ads, messages, pitch crafting"),
    ("credit_repair", "💳 Credit Repair", "Portal to your credit repair SaaS")
]

# Write main app and auth logic
write_file("app.py", app_py)
write_file("backend/auth.py", auth_py)

# Write 16 folder-based tab modules
for folder, label, desc in tabs:
    tab_code = f'''import streamlit as st

def run():
    st.title("{label}")
    st.markdown("### {desc}")
    st.info("This section is ready for enhancements like export, GPT, or Sheets.")
'''
    write_file(f"{folder}/{folder}_app.py", tab_code)

print("✅ FINAL BUILD READY — All folders, app.py, auth, and 16 working tab modules are in place!")
