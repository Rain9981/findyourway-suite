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

    st.title("🧠 CRM Insights")
    st.markdown("Paste in notes from a client session to receive smart AI feedback.")

    st.sidebar.header("💡 CRM Insights Guide")
    st.sidebar.markdown("""
    - Use this to analyze or summarize your client interactions.
    - Add client name and session notes.
    - GPT will extract insights and suggestions.
    - Admins can export results to PDF.
    """)

    default_prompt = "Client was unsure about pricing. They liked the service but hesitant about monthly commitment."

    if "crm_insights_autofill_triggered" not in st.session_state:
        st.session_state["crm_insights_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="crm_insights_autofill"):
        st.session_state["crm_insights_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["crm_insights_autofill_triggered"] else ""

    client_name = st.text_input("Client Name:", key="crm_insights_name")
    session_notes = st.text_area("Paste session notes:", value=input_value, key="crm_insights_input")

    if st.button("🚀 Analyze Notes with GPT", key="crm_insights_run") and session_notes:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business consultant who provides insights based on CRM session notes."},
                    {"role": "user", "content": session_notes}
                ]
            )
            insights = response.choices[0].message.content.strip()
            st.session_state["crm_insights_result"] = insights
            st.success(insights)
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
                ws = sheet.worksheet("CRM Insights")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="CRM Insights", rows="100", cols="20")
                ws.append_row(["Timestamp", "Client Name", "Notes", "Insights"])

            ws.append_row([
                str(datetime.datetime.now()),
                client_name,
                session_notes,
                insights
            ])
            st.info("✅ Saved to Google Sheets.")
        except Exception as e:
            st.warning(f"⚠️ Google Sheets not connected: {e}")

        # Admin PDF Export
        if st.session_state.get("user_role", "guest") == "admin":
            if st.button("📄 Export to PDF", key="crm_insights_pdf"):
                buffer = io.BytesIO()
                c = pdf_canvas.Canvas(buffer, pagesize=letter)
                c.drawString(100, 750, "CRM Insight Report")
                c.drawString(100, 735, f"Client: {client_name}")
                c.drawString(100, 715, "Notes:")
                text = c.beginText(100, 700)
                for line in session_notes.splitlines():
                    text.textLine(line[:100])
                c.drawText(text)
                c.drawString(100, 650, "GPT Insights:")
                insight_text = c.beginText(100, 635)
                for line in insights.splitlines():
                    insight_text.textLine(line[:100])
                c.drawText(insight_text)
                c.save()
                buffer.seek(0)
                st.download_button("Download PDF", buffer, file_name=f"{client_name}_insights_report.pdf")
