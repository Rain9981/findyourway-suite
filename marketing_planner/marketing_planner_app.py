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
    st.title("📅 Marketing Planner")
    st.markdown("### Plan campaigns, calendars, and content ideas.")

    st.sidebar.header("💡 Marketing Planner Guide")
    st.sidebar.write("**What this tab does:** Helps map out marketing campaigns, ads, or promotions.")
    st.sidebar.write("**What to input:** Enter a time frame, product, and audience.")
    st.sidebar.write("**How to use:** GPT returns campaign themes, content calendars, or ad angles.")

    example_prompt = "Plan a 2-week launch campaign for a fitness coaching app targeting working moms."
    user_input = st.text_area("Describe your marketing goal or plan:", value=example_prompt, key="marketing_planner_input")

    if st.button("Generate Plan", key="marketing_planner_autofill") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a marketing strategist helping design smart campaigns."},
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
            worksheet = sheet.worksheet("marketing planner")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="marketing planner", rows="100", cols="20")
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

    if st.button("Export to PDF", key="marketing_planner_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Marketing Planner Report")
        c.drawString(100, 735, f"Plan: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="marketing_planner_report.pdf")
