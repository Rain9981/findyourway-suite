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
    st.title("📈 Growth Strategy")
    st.markdown("### Explore ways to scale your business or personal impact.")

    st.sidebar.header("💡 Growth Strategy Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you explore ways to grow your business or audience.
    - **What to enter:** A goal or area where you'd like to see growth.
    - **How to use:** Use the AI to get ideas and actions you can take.
    """)

    default_prompt = "How can I grow my consulting business in the digital space?"

    if "growth_autofill_triggered" not in st.session_state:
        st.session_state["growth_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="growth_autofill"):
        st.session_state["growth_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["growth_autofill_triggered"] else ""

    user_input = st.text_area(
        "Describe your growth goal or business area to improve:",
        value=input_value,
        key="growth_input"
    )

    if st.button("🚀 Run GPT-4o Autofill", key="growth_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business strategist helping users identify growth strategies."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    # ✅ Save to Google Sheets
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Growth")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Growth", rows="100", cols="20")

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

    if st.button("📄 Export to PDF", key="growth_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Growth Strategy Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="growth_report.pdf")
