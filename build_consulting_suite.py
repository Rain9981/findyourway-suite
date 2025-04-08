
import os

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# Base folders
folders = [
    "tabs",
    "backend",
    "assets",
    ".streamlit",
    "guides"
]

# Create base structure
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Main app launcher
write_file("app.py", """import streamlit as st
from backend.auth import check_login, get_user_role
from tabs import (
    forecasting, sentiment, simulator, intake, brand_positioning, business_plan,
    leads, crm, kpi, funnel, email, audit, social, credit, toolkit, admin_settings
)
from PIL import Image

# Logo + globe animation
st.set_page_config(page_title="Find Your Way Consulting Suite", page_icon="💼")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Globe animation
st.markdown(
    '<div style="text-align:center;"><img src="https://i.gifer.com/7VE.gif" width="150"/></div>',
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
""")

# requirements.txt
write_file("requirements.txt", "streamlit\npandas\nreportlab\ngspread\noauth2client\nopenpyxl")

# README
write_file("README.md", "# Find Your Way Consulting Suite\n\nTo run: streamlit run app.py")

# Secrets template
write_file(".streamlit/secrets.toml", "[google_sheets]\nsheet_id = \"your_google_sheet_id_here\"\nservice_account = \"\"\n\n[email]\nsmtp_user = \"\"\nsmtp_password = \"\"\n\n[admin]\npassword = \"FindYourWayNMC520\"")

# Auth logic
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

# Tab boilerplate
tab_names = [
    "forecasting", "sentiment", "simulator", "intake", "brand_positioning",
    "business_plan", "leads", "crm", "kpi", "funnel", "email", "audit",
    "social", "credit", "toolkit", "admin_settings"
]

for name in tab_names:
    write_file(f"tabs/{name}.py", f"""import streamlit as st

def run():
    st.title("{name.replace('_', ' ').title()}")
    st.write("This is the {name.replace('_', ' ').title()} tab.")
""")

# Backend placeholders
for module in ["crm", "export", "google_sheets"]:
    write_file(f"backend/{module}.py", f"# Logic for {module}")

# Guides
write_file("guides/consulting_walkthrough.md", "# How to Consult Clients Using the Suite\n\nInstructions for each tab based on tier.")
write_file("guides/client_reference_table.csv", "Field Name,Description\nBusiness Name,The name of the client's business\nIndustry,Their target industry")

print("✅ Build complete! Your consulting suite is ready.")
