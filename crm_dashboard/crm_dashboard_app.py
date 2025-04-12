import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

st.title("📊 CRM Dashboard")
st.markdown("Overview of your client base with basic stats and trends.")

st.sidebar.header("💡 Dashboard Tips")
st.sidebar.markdown("""
- Visualize total clients and status breakdown.
- Use this tab for consulting KPIs and summary metrics.
""")

# Load data
def get_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
    try:
        ws = sheet.worksheet("CRM Manager")
    except WorksheetNotFound:
        return []
    return ws.get_all_records()

try:
    data = get_data()
    total = len(data)
    active = sum(1 for d in data if d.get("Status") == "Active")
    leads = sum(1 for d in data if d.get("Status") == "Lead")
    inactive = sum(1 for d in data if d.get("Status") == "Inactive")

    st.metric("Total Clients", total)
    st.metric("Active Clients", active)
    st.metric("Leads", leads)
    st.metric("Inactive Clients", inactive)

    if total > 0:
        st.markdown("### 📋 Raw CRM Data")
        st.dataframe(data, use_container_width=True)
except Exception as e:
    st.warning(f"⚠️ Could not load CRM data: {e}")
