import streamlit as st
from openai import OpenAI
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🌐 Network Builder")
    st.markdown("### Design a strategy to build relationships and partnerships.")

    st.sidebar.header("💡 Network Builder Guide")
    st.sidebar.write("**What this tab does:** Helps you grow a professional or customer network.")
    st.sidebar.write("**What to enter:** Describe who you're trying to reach or build partnerships with.")
    st.sidebar.write("**How to use it:** GPT will suggest outreach ideas, platforms, or engagement plans.")

    user_input = st.text_area("Who are you trying to network with?", key="network_builder_input")

    if st.button("Build Network Strategy", key="network_builder_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business networking consultant helping users build meaningful connections."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    # ✅ Save to Google Sheets (prevent duplicate sheet error)
    try:
        from gspread.exceptions import WorksheetNotFound
        import gspread
        import json
        import datetime
        from oauth2client.service_account import ServiceAccountCredentials

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Network Builder")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Network Builder", rows="100", cols="20")

        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input"])

        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    # ✅ PDF Export
    if st.button("Export to PDF", key="network_builder_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Network Builder Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_builder_report.pdf")
