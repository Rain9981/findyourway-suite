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

    st.title("📬 Email Marketing")
    st.markdown("Craft or improve your marketing email campaigns with AI support.")

    st.sidebar.header("💡 Email Marketing Guide")
    st.sidebar.markdown("""
    - Use this tool to write or refine marketing emails.
    - Describe your campaign or paste a draft.
    - Use GPT to improve tone, clarity, and effectiveness.
    - Admins can export results as PDF.
    """)

    default_prompt = "We want to promote our new virtual coaching program to previous leads via email."

    if "email_marketing_autofill_triggered" not in st.session_state:
        st.session_state["email_marketing_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="email_marketing_autofill"):
        st.session_state["email_marketing_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["email_marketing_autofill_triggered"] else ""

    email_input = st.text_area("Describe your campaign or paste a draft email:", value=input_value, key="email_marketing_input")

    if st.button("🚀 Generate Email with GPT-4o", key="email_marketing_run") and email_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a marketing copywriter crafting engaging promotional emails."},
                    {"role": "user", "content": email_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.success(result)
            st.session_state["email_marketing_result"] = result
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

        # Save to Google Sheets
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            client_gsheets = gspread.authorize(credentials)
            sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Email Marketing")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Email Marketing", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "GPT Email Result"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                email_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")
        except Exception as e:
            st.warning(f"Google Sheets not connected: {e}")

        # PDF Export
        if st.session_state.get("user_role", "guest") == "admin":
            if st.button("📄 Export to PDF", key="email_marketing_pdf"):
                buffer = io.BytesIO()
                c = pdf_canvas.Canvas(buffer, pagesize=letter)
                c.drawString(100, 750, "Email Marketing Campaign")
                c.drawString(100, 730, f"Original Input: {email_input[:90]}")
                c.drawString(100, 710, "GPT Email:")
                text = c.beginText(100, 695)
                for line in result.splitlines():
                    text.textLine(line[:100])
                c.drawText(text)
                c.save()
                buffer.seek(0)
                st.download_button("Download PDF", buffer, file_name="email_campaign.pdf")
