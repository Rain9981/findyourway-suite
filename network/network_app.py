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
    st.title("🌐 Network")
    st.markdown("### Build and expand your strategic connections.")

    st.sidebar.header("💡 Network Builder Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps brainstorm strategic connections and collaborations.
    - **What to enter:** Describe your business, industry, or target network.
    - **How to use:** Use GPT to suggest networking strategies, then save/export.
    """)

    default_prompt = "I want to connect with small business owners in the wellness industry."

    if "network_autofill_triggered" not in st.session_state:
        st.session_state["network_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="network_autofill"):
        st.session_state["network_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["network_autofill_triggered"] else ""

    user_input = st.text_area(
        "Who are you trying to connect with and why?",
        value=input_value,
        key="network_input"
    )

    if st.button("🚀 Run GPT-4o Autofill", key="network_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a network strategist helping build valuable business relationships."},
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
            worksheet = sheet.worksheet("Network")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Network", rows="100", cols="20")

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

    if st.button("📄 Export to PDF", key="network_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Network Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_report.pdf")
