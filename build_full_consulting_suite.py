
import os

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# --- Folder structure ---
folders = [
    "tabs", "backend", ".streamlit", "assets", "guides"
]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# --- app.py with login, tier logic, and spinning globe ---
app_code = """import streamlit as st
from backend.auth import check_login, get_user_role
from tabs import (
    forecasting, sentiment, simulator, intake, brand_positioning, business_plan,
    leads, crm, kpi, funnel, email, audit, social, credit, toolkit, admin_settings
)

st.set_page_config(page_title="Find Your Way Consulting Suite", page_icon="💼")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Globe animation
st.markdown(
    '''
    <div style="text-align:center; margin-top: 10px;">
        <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" width="120" alt="Loading Globe"/>
    </div>
    ''',
    unsafe_allow_html=True
)

# Login
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
    if role == "Basic":
        tabs = ["Forecasting", "Sentiment", "Simulator", "Client Intake", "Brand Map"]
    elif role == "Elit":
        tabs = ["Forecasting", "Sentiment", "Simulator", "Client Intake", "Brand Map",
                "Business Plan", "Lead Generator", "CRM", "KPI", "Funnel", "Email", "Audit"]
    elif role == "Premium":
        tabs = ["Forecasting", "Sentiment", "Simulator", "Client Intake", "Brand Map",
                "Business Plan", "Lead Generator", "CRM", "KPI", "Funnel", "Email", "Audit"]
    elif role == "Admin":
        tabs = ["Forecasting", "Sentiment", "Simulator", "Client Intake", "Brand Map",
                "Business Plan", "Lead Generator", "CRM", "KPI", "Funnel", "Email", "Audit",
                "Social Media", "Credit Repair", "Marketing Toolkit", "Admin Panel"]

    choice = st.selectbox("📊 Choose a tool", tabs)

    match choice:
        case "Forecasting": forecasting.run()
        case "Sentiment": sentiment.run()
        case "Simulator": simulator.run()
        case "Client Intake": intake.run()
        case "Brand Map": brand_positioning.run()
        case "Business Plan": business_plan.run()
        case "Lead Generator": leads.run()
        case "CRM": crm.run()
        case "KPI": kpi.run()
        case "Funnel": funnel.run()
        case "Email": email.run()
        case "Audit": audit.run()
        case "Social Media": social.run()
        case "Credit Repair": credit.run()
        case "Marketing Toolkit": toolkit.run()
        case "Admin Panel": admin_settings.run()
"""

write_file("app.py", app_code)
write_file("requirements.txt", "streamlit\npandas\nreportlab\ngspread\noauth2client\nopenpyxl\n")
write_file("README.md", "# Find Your Way Consulting Suite\n\nTo run: streamlit run app.py")

# --- Secrets ---
write_file(".streamlit/secrets.toml", "[google_sheets]\nsheet_id = \"your_google_sheet_id_here\"\nservice_account = \"\"\n\n[email]\nsmtp_user = \"\"\nsmtp_password = \"\"\n\n[admin]\npassword = \"FindYourWayNMC520\"")

# --- Auth logic ---
write_file("backend/auth.py", """def check_login(username, password):
    users = {
        "basicuser": {"password": "basic123", "role": "Basic"},
        "elituser": {"password": "elit123", "role": "Elit"},
        "premiumuser": {"password": "premium123", "role": "Premium"},
        "admin": {"password": "FindYourWayNMC520", "role": "Admin"}
    }
    return username in users and users[username]["password"] == password

def get_user_role(username):
    users = {
        "basicuser": {"password": "basic123", "role": "Basic"},
        "elituser": {"password": "elit123", "role": "Elit"},
        "premiumuser": {"password": "premium123", "role": "Premium"},
        "admin": {"password": "FindYourWayNMC520", "role": "Admin"}
    }
    return users[username]["role"]
""")

# Placeholder: Part 2 will drop real logic into tabs + backend files next
print("✅ Base structure and login created. Run part 2 to populate tools.")
