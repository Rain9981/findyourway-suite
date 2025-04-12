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
    st.title("🧩 Business Model Canvas")
    st.markdown("Use AI to build a strategic business model canvas for your idea or venture.")

    st.sidebar.header("💡 Canvas Guide")
    st.sidebar.markdown("""
    - Describe your business concept or product.
    - GPT will turn it into a canvas-style summary (customer segments, value prop, channels, etc.).
    - Save to Sheets or export to PDF.
    """)

    default_prompt = "I'm launching a mobile car detailing service targeting busy professionals in urban areas."

    if "canvas_autofill_triggered" not in st.session_state:
        st.session_state["canvas_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="canvas_autofill"):
        st.session_state["canvas_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["canvas_autofill_triggered"] else ""

    user_input = st.text_area("Describe your business or idea:", value=input_value, key="canvas_input")

    if st.button("🚀 Generate Canvas with GPT-4o", key="canvas_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a strategist building business model canvases. Use the 9-block format (Key Partners, Activities, Resources, Value Proposition, Customer Relationships, Channels, Customer Segments, Cost Structure, Revenue Streams)."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["canvas_result"] = result
            st.subheader("📋 Business Model Canvas")
            st.success(result)

            # Google Sheets save
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Business Model Canvas")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Business Model Canvas", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "Canvas Output"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")
            
            # PDF export
            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="canvas_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Business Model Canvas Summary")
                    c.drawString(100, 730, f"Input: {user_input[:90]}")
                    c.drawString(100, 710, "Canvas:")
                    text = c.beginText(100, 695)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="business_model_canvas.pdf")
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")
