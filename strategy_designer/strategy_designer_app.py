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
    st.title("🧠 Strategy Designer")
    st.markdown("Use this tool to brainstorm or refine business strategies.")

    st.sidebar.header("💡 Strategy Tips")
    st.sidebar.markdown("""
    - Enter a goal, challenge, or business opportunity.
    - GPT will give you a strategic plan or decision framework.
    """)

    default_prompt = "How can we increase our monthly recurring revenue without raising prices?"

    if "strategy_designer_autofill_triggered" not in st.session_state:
        st.session_state["strategy_designer_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="strategy_designer_autofill"):
        st.session_state["strategy_designer_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["strategy_designer_autofill_triggered"] else ""

    user_input = st.text_area("Enter your strategic challenge or goal:", value=input_value, key="strategy_designer_input")

    if st.button("🚀 Design Strategy with GPT-4o", key="strategy_designer_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business strategist. Help design a path forward for this goal."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["strategy_designer_result"] = result
            st.subheader("📋 GPT-Generated Strategy")
            st.success(result)

            # Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Strategy Designer")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Strategy Designer", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "GPT Result"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")

            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="strategy_designer_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Strategy Designer Summary")
                    c.drawString(100, 730, f"Input: {user_input[:90]}")
                    text = c.beginText(100, 710)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="strategy_summary.pdf")
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")
