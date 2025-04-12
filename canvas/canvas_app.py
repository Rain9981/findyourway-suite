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
    st.title("🧩 Business Canvas Builder")
    st.markdown("### Enter your business idea or concept to generate a strategic canvas.")

    st.sidebar.header("💡 Canvas Builder Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Builds a business model canvas from your idea.
    - **What to enter:** Your product, service, or business concept.
    - **How to use:** Paste your idea or use autofill. GPT will generate canvas-style guidance.
    """)

    default_prompt = "I’m starting a mobile car detailing service in urban neighborhoods. I need a business model canvas."

    if "canvas_autofill_triggered" not in st.session_state:
        st.session_state["canvas_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="canvas_autofill"):
        st.session_state["canvas_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["canvas_autofill_triggered"] else ""

    user_input = st.text_area("Describe your business idea:", value=input_value, key="canvas_input")

    if st.button("🚀 Generate Canvas", key="canvas_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a strategist building business model canvases."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["canvas_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["canvas_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])
        try:
            worksheet = sheet.worksheet("Canvas")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Canvas", rows="100", cols="20")
        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input", "Canvas Result"])
        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("canvas_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="canvas_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Business Canvas Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('canvas_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="business_canvas_report.pdf")
