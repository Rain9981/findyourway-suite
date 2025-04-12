import streamlit as st
import datetime
import json
import io
import gspread
from openai import OpenAI  # ✅ FIXED: added OpenAI import
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    st.title("🏗️ Business Development")
    st.markdown("Identify partnership, expansion, and growth opportunities.")

    st.sidebar.header("💡 Biz Dev Guide")
    st.sidebar.markdown("""
    - Describe your current growth goal or new market you're exploring.
    - GPT will help you brainstorm smart strategies.
    - Save to Sheets or export to PDF if you're an admin.
    """)

    default_prompt = "We want to partner with fitness brands to cross-promote our meal plan app."

    if "business_dev_autofill_triggered" not in st.session_state:
        st.session_state["business_dev_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="business_dev_autofill"):
        st.session_state["business_dev_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["business_dev_autofill_triggered"] else ""

    user_input = st.text_area("Describe your growth idea or partnership goal:", value=input_value, key="business_dev_input")

    if st.button("🚀 Run GPT-4o Strategy", key="business_dev_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business strategist. Help refine this growth or partnership idea."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["business_dev_result"] = result
            st.subheader("📈 GPT-Generated Business Strategy")
            st.success(result)

            # Save to Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Business Development")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Business Development", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "Result"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")

            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="business_dev_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Business Development Summary")
                    c.drawString(100, 730, f"Input: {user_input[:80]}")
                    c.drawString(100, 710, "GPT Output:")
                    text = c.beginText(100, 695)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="business_development.pdf")
        except Exception as e:
            st.error(f"❌ Error: {e}")
