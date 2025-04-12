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
    st.title("📈 Business Forecasting")
    st.markdown("### Describe your future plans, projections, or growth expectations.")

    st.sidebar.header("💡 Forecasting Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you predict and strategize using AI insights.
    - **What to enter:** Describe growth expectations, forecasts, or trends.
    - **How to use:** Use suggestion or type in your forecast. Click GPT-4o to generate insights.
    """)

    default_prompt = "We expect revenue to increase 15% in Q4 due to seasonal demand and promotions."

    if "forecasting_autofill_triggered" not in st.session_state:
        st.session_state["forecasting_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="forecasting_autofill"):
        st.session_state["forecasting_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["forecasting_autofill_triggered"] else ""

    user_input = st.text_area("Describe your forecast:", value=input_value, key="forecasting_input")

    if st.button("🚀 Run GPT-4o Analysis", key="forecasting_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a forecasting and business trend expert."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["forecasting_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["forecasting_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Forecasting")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Forecasting", rows="100", cols="20")

        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input", "AI Result"])

        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("forecasting_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="forecasting_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Forecasting Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('forecasting_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="forecasting_report.pdf")
