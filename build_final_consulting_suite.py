import os

def write_file(path, content):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


app_code = '''import streamlit as st
from backend.auth import check_login, get_user_role
import importlib

st.set_page_config(page_title="Find Your Way Consulting Suite", page_icon="💼")

# Branding: logo and globe
st.markdown(\"\"\"
<div style="text-align:center; margin-top: 10px;">
    <img src="https://i.gifer.com/7VE.gif" width="100"/>
</div>
\"\"\", unsafe_allow_html=True)

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
'''

# Write the app launcher
write_file("app.py", app_code)

# Write auth backend
write_file("backend/auth.py", '''def check_login(username, password):
    users = {
        "basic": {"password": "basic123", "role": "Basic"},
        "elite": {"password": "elite123", "role": "Elite"},
        "premium": {"password": "premium123", "role": "Premium"},
        "admin": {"password": "FindYourWayNMC520", "role": "Admin"}
    }
    return username in users and users[username]["password"] == password

def get_user_role(username):
    users = {
        "basic": {"password": "basic123", "role": "Basic"},
        "elite": {"password": "elite123", "role": "Elite"},
        "premium": {"password": "premium123", "role": "Premium"},
        "admin": {"password": "FindYourWayNMC520", "role": "Admin"}
    }
    return users[username]["role"]
''')

# Folders and base tab apps
tabs = {
    "forecasting": "Business forecast simulator",
    "sentiment_analysis": "AI-powered market sentiment analyzer",
    "strategic_simulator": "Simulate strategic business decisions",
    "client_intake": "New client onboarding form",
    "brand_positioning": "Define brand messaging and market fit",
    "kpi_tracker": "Track business KPIs and goals",
    "strategy_designer": "Design long-term business strategies",
    "business_model_canvas": "Visualize your business structure",
    "operations_audit": "Review internal systems and workflows",
    "lead_generation": "Generate leads and export results",
    "crm_manager": "Client relationship tracking",
    "network_builder": "Build network maps and referrals",
    "business_development": "Growth templates and planning",
    "self_enhancement": "Founder self-improvement tracker",
    "marketing_hub": "Marketing message builder and templates",
    "credit_repair": "Credit repair portal integration"
}

for folder, desc in tabs.items():
    tab_code = f'''import streamlit as st

def run():
    st.title("{desc}")
    st.markdown("This section will be enhanced with OpenAI, Sheets, or PDF export.")
'''
    write_file(f"{folder}/{folder}_app.py", tab_code)

print("✅ FINAL BUILD COMPLETE — All folders, logic, branding, and tiers set.")
