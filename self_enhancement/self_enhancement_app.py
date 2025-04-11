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
    st.title("🌱 Self Enhancement")
    st.markdown("### Explore ways to grow your personal and professional self.")

    st.sidebar.header("💡 Self Enhancement Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Suggests ideas for personal growth and self-improvement.
    - **What to enter:** Goals, habits, mindset shifts, or growth challenges.
    - **How to use:** Use GPT to brainstorm self-enhancement plans, export your ideas, or save to Sheets.
    """)

    default_prompt = "I want to improve my time management and confidence."
    user_input = st.text_area(
        "What aspect of your personal or professional self are you improving?",
        value=default_prompt,
        key="self_enhancement_input"
    )

    if st.button("✨ Autofill Suggestion", key="self_enhancement_autofill"):
        st.session_state.self_enhancement_input = default_prompt

    if st.button("🚀 Run GPT-4o Autofill", key="self_enhancement_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a personal development coach helping someone enhance their mindset, skills, or habits."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    # ✅ Google Sheets Save Logic (safe from duplicate tab error)
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Self Enhancement")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Self Enhancement", rows="100", cols="20")

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

    # 🧾 PDF Export
    if st.button("📄 Export to PDF", key="self_enhancement_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Self Enhancement Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="self_enhancement_report.pdf")
