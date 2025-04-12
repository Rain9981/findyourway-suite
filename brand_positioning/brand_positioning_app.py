import streamlit as st
import datetime
import json
import io
import gspread
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    st.title("🏷️ Brand Positioning")
    st.markdown("Define your unique market position and clarify your brand identity.")

    st.sidebar.header("💡 Brand Positioning Guide")
    st.sidebar.markdown("""
    - Describe what your brand stands for, who it's for, and how it's different.
    - GPT will help you sharpen your positioning statement.
    - Save to Sheets or export as PDF (admin only).
    """)

    default_prompt = "We are a luxury skincare brand that uses clean ingredients and targets women over 40 who value wellness."

    if "brand_positioning_autofill_triggered" not in st.session_state:
        st.session_state["brand_positioning_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="brand_positioning_autofill"):
        st.session_state["brand_positioning_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["brand_positioning_autofill_triggered"] else ""

    user_input = st.text_area("Describe your brand and ideal market:", value=input_value, key="brand_positioning_input")

    if st.button("🚀 Generate Positioning with GPT-4o", key="brand_positioning_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a branding consultant. Help define a strong, clear brand positioning statement."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["brand_positioning_result"] = result
            st.subheader("🧭 GPT-Generated Brand Positioning")
            st.success(result)

            # Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Brand Positioning")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Brand Positioning", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "Result"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")

            # PDF export
            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="brand_positioning_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Brand Positioning Summary")
                    c.drawString(100, 730, f"Input: {user_input[:80]}")
                    c.drawString(100, 710, "GPT Output:")
                    text = c.beginText(100, 695)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="brand_positioning.pdf")
        except Exception as e:
            st.error(f"❌ Error: {e}")
