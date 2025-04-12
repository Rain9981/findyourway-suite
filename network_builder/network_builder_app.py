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
    st.title("🌐 Network Builder")
    st.markdown("### Describe who you're trying to connect with or your networking goal.")

    st.sidebar.header("💡 Networking Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you build strategic relationships and outreach ideas.
    - **What to enter:** Your niche, target partners, or networking goals.
    - **How to use:** Type your goal or use the suggestion, then click GPT to get strategic outreach steps.
    """)

    default_prompt = "I want to connect with marketing experts to grow partnerships and gain referrals."

    if "network_builder_autofill_triggered" not in st.session_state:
        st.session_state["network_builder_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="network_builder_autofill"):
        st.session_state["network_builder_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["network_builder_autofill_triggered"] else ""

    user_input = st.text_area("What is your networking goal?", value=input_value, key="network_builder_input")

    if st.button("🚀 Generate Outreach Plan", key="network_builder_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business networking strategist helping people build strong relationships."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["network_builder_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["network_builder_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
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
            worksheet.append_row(["Timestamp", "User Role", "Input", "GPT Result"])

        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("network_builder_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="network_builder_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Networking Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('network_builder_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_builder_report.pdf")
