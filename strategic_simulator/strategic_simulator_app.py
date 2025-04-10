import streamlit as st
from openai import OpenAI
import io
import datetime
import gspread
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
import json

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧮 Strategic Simulator")
    st.markdown("### Simulate outcomes from business decisions.")

    st.sidebar.header("💡 Strategic Simulator Guide")
    st.sidebar.write("**What this tab does:** Simulates possible outcomes based on a business decision or direction.")
    st.sidebar.write("**What to input:** Enter a scenario like launching a product, changing prices, or entering new markets.")
    st.sidebar.write("**How to use:** Use GPT to predict outcomes and strategy pivots.")

    example_prompt = "What could happen if we raised our subscription pricing by 15% next quarter?"
    user_input = st.text_area("Enter your scenario to simulate:", value=example_prompt, key="strategic_simulator_input")

    if st.button("Run Simulation", key="strategic_simulator_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a strategic AI simulating business decision outcomes."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])
        try:
            worksheet = sheet.worksheet("strategic simulator")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="strategic simulator", rows="100", cols="20")
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

    if st.button("Export to PDF", key="strategic_simulator_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Strategic Simulator Report")
        c.drawString(100, 735, f"Scenario: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="strategic_simulator_report.pdf")
