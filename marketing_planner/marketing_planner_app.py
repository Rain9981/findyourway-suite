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
    st.title("📣 Marketing Planner")
    st.markdown("### Describe your campaign or goal to generate a strategy.")

    st.sidebar.header("💡 Marketing Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you build a tailored marketing campaign.
    - **What to enter:** Business goal or product you want to promote.
    - **How to use:** Use autofill or describe your needs, then generate strategy with GPT.
    """)

    default_prompt = "I want to promote a new digital course for busy moms using social media and email marketing."

    if "marketing_planner_autofill_triggered" not in st.session_state:
        st.session_state["marketing_planner_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="marketing_planner_autofill"):
        st.session_state["marketing_planner_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["marketing_planner_autofill_triggered"] else ""

    user_input = st.text_area("Describe your marketing campaign goal:", value=input_value, key="marketing_planner_input")

    if st.button("🚀 Generate Strategy", key="marketing_planner_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a marketing strategist helping plan campaigns."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["marketing_planner_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["marketing_planner_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])
        try:
            worksheet = sheet.worksheet("Marketing Planner")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Marketing Planner", rows="100", cols="20")
        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input", "AI Result"])
        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("marketing_planner_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="marketing_planner_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Marketing Strategy Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('marketing_planner_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="marketing_strategy_report.pdf")
