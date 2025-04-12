import streamlit as st
import datetime
import json
import io
import gspread
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

st.title("🧾 CRM Manager")
st.markdown("Use this form to add new clients and view your full contact list.")

st.sidebar.header("💡 CRM Manager Tips")
st.sidebar.markdown("""
- Add new clients with the form below.
- Entries save directly to Google Sheets.
- View all clients in the table.
- Admins can export any row to PDF.
""")

# Google Sheets Setup
def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
    try:
        ws = sheet.worksheet("CRM Manager")
    except WorksheetNotFound:
        ws = sheet.add_worksheet(title="CRM Manager", rows="100", cols="20")
        ws.append_row(["Timestamp", "Name", "Email", "Phone", "Status", "Notes"])
    return ws

# Add client form
with st.form("add_client_form"):
    name = st.text_input("Client Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    status = st.selectbox("Status", ["Lead", "Active", "Inactive"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Client")
    if submitted and name:
        ws = get_worksheet()
        ws.append_row([
            str(datetime.datetime.now()), name, email, phone, status, notes
        ])
        st.success(f"✅ {name} added to CRM.")

# Show table
try:
    ws = get_worksheet()
    data = ws.get_all_values()
    headers, rows = data[0], data[1:]
    st.markdown("### 📋 All Clients")
    st.dataframe(rows, use_container_width=True)

    # Export to PDF for admins
    if st.session_state.get("user_role", "guest") == "admin":
        selected_name = st.selectbox("Select a client to export:", [r[1] for r in rows])
        if st.button("📄 Export Selected to PDF"):
            match = next((r for r in rows if r[1] == selected_name), None)
            if match:
                buffer = io.BytesIO()
                c = pdf_canvas.Canvas(buffer, pagesize=letter)
                c.drawString(100, 750, "Client Summary")
                for i, val in enumerate(match):
                    c.drawString(100, 730 - i * 15, f"{headers[i]}: {val}")
                c.save()
                buffer.seek(0)
                st.download_button("Download PDF", buffer, file_name=f"{selected_name}_CRM.pdf")
except Exception as e:
    st.warning(f"Google Sheets not connected: {e}")
