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
    st.title("📝 Client Intake")
    st.markdown("### Start here to collect key client information and goals.")

    st.sidebar.header("💡 Intake Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Collects initial client context, goals, and business type.
    - **What to enter:** Business name, industry, goals, challenges, and services they need.
    - **How to use:** Autofill to try a sample or describe your client needs and save.
    """)

    default_prompt = "A new client named Vital Wellness wants help scaling their fitness brand online."

    # Track autofill trigger
    if "client_intake_autofill_triggered" not in st.session_state:
        st.session_state["client_intake_autofill_triggered"] = False

    # Autofill button
    if st.button("✨ Autofill Suggestion", key="client_intake_autofill"):
        st.session_state["client_intake_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["client_intake_autofill_triggered"] else ""

    user_input = st.text_area(
        "Describe your client’s business or request:",
        value=input_value,
        key="client_intake_input"
    )

    if st.button("🚀 Run GPT-4o Autofill", key="client_intake_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're an expert intake assistant. Help summarize client needs and guide next steps."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    # Save to Google Sheets (safe)
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Client Intake")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Client Intake", rows="100", cols="20")

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

    # PDF Export
    if st.button("📄 Export to PDF", key="client_intake_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Client Intake Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="client_intake_report.pdf")
