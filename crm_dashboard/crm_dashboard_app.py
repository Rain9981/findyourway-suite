import streamlit as st
import json
import io
import gspread
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

def run():
    st.title("📊 CRM Dashboard")
    st.markdown("Client overview and activity summary pulled from CRM Manager.")

    st.sidebar.header("💡 Dashboard Tips")
    st.sidebar.markdown("""
    - View your total client counts and statuses.
    - Raw data is pulled from CRM Manager.
    - Admins can export this summary as a PDF report.
    """)

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

        # PDF Export (Admin Only)
        if st.session_state.get("user_role", "guest") == "admin":
            if st.button("📄 Export Dashboard to PDF"):
                buffer = io.BytesIO()
                c = pdf_canvas.Canvas(buffer, pagesize=letter)
                c.drawString(100, 750, "CRM Dashboard Summary")
                c.drawString(100, 730, f"Total Clients: {total}")
                c.drawString(100, 715, f"Active: {active} | Leads: {leads} | Inactive: {inactive}")
                c.drawString(100, 695, "Recent Clients:")
                preview = data[:5]
                for i, row in enumerate(preview):
                    line = f"{i+1}. {row.get('Name', '')} - {row.get('Status', '')} - {row.get('Email', '')}"
                    c.drawString(100, 675 - i * 15, line[:100])
                c.save()
                buffer.seek(0)
                st.download_button("Download CRM Summary PDF", buffer, file_name="crm_dashboard_summary.pdf")

    except Exception as e:
        st.warning(f"⚠️ Could not load CRM data: {e}")
