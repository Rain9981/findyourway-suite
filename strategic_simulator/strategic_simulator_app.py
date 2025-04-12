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
    st.title("♟️ Strategic Simulator")
    st.markdown("### Simulate business decisions and predict possible outcomes.")

    st.sidebar.header("💡 Simulator Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Simulates scenarios to test business strategy ideas.
    - **What to enter:** Describe a business decision or situation you want to test.
    - **How to use:** Use the autofill or describe your scenario. Click run to simulate outcomes with AI help.
    """)

    default_prompt = "If we lower product prices by 10%, how might it affect revenue and customer loyalty?"

    if "strategic_simulator_autofill_triggered" not in st.session_state:
        st.session_state["strategic_simulator_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="strategic_simulator_autofill"):
        st.session_state["strategic_simulator_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["strategic_simulator_autofill_triggered"] else ""

    user_input = st.text_area("Describe your business scenario to simulate:", value=input_value, key="strategic_simulator_input")

    if st.button("🚀 Run GPT-4o Simulation", key="strategic_simulator_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business strategist simulating outcomes of key decisions."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["strategic_simulator_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["strategic_simulator_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Strategic Simulator")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Strategic Simulator", rows="100", cols="20")

        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input", "Simulation Result"])

        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("strategic_simulator_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="strategic_simulator_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Strategic Simulation Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('strategic_simulator_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="strategic_simulation_report.pdf")
