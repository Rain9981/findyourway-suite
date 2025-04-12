import streamlit as st
from openai import OpenAI
import io
import datetime
import json
import gspread
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🚨 Oops Audit")
    st.markdown("### Describe a mistake or challenge in your business to get insight.")

    st.sidebar.header("💡 Audit Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you audit mistakes and turn them into lessons.
    - **What to enter:** A problem, failure, or mistake in your business.
    - **How to use:** Enter your challenge and GPT will help you reframe and improve.
    """)

    default_prompt = "We launched a product without testing and got bad reviews. What can we learn and how can we recover?"

    if "oops_audit_autofill_triggered" not in st.session_state:
        st.session_state["oops_audit_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="oops_audit_autofill"):
        st.session_state["oops_audit_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["oops_audit_autofill_triggered"] else ""

    user_input = st.text_area("Describe a business mistake or issue:", value=input_value, key="oops_audit_input")

    if st.button("🚀 Run GPT-4o Audit", key="oops_audit_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business consultant helping turn failures into strategies."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["oops_audit_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["oops_audit_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])
        try:
            worksheet = sheet.worksheet("Oops Audit")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Oops Audit", rows="100", cols="20")
        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input", "AI Result"])
        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("oops_audit_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="oops_audit_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Oops Audit Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('oops_audit_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="oops_audit_report.pdf")
