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

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.title("🧠 CRM Insights")
st.markdown("Paste in notes from a client session to receive smart AI feedback.")

st.sidebar.header("💡 CRM Insights Guide")
st.sidebar.markdown("""
- Use this to analyze or summarize your client interactions.
- Add client name and session notes.
- GPT will extract insights and suggestions.
""")

default_prompt = "Spoke with client about pricing hesitations. They mentioned feeling unsure about the timeline and ROI."

if "crm_autofill_triggered" not in st.session_state:
    st.session_state["crm_autofill_triggered"] = False

if st.button("✨ Autofill Example", key="crm_autofill"):
    st.session_state["crm_autofill_triggered"] = True

input_value = default_prompt if st.session_state["crm_autofill_triggered"] else ""

name = st.text_input("Client Name:", key="crm_name")
notes = st.text_area("Paste session notes:", value=input_value, key="crm_input")

if st.button("🚀 Analyze Notes", key="crm_run") and notes:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a client success strategist. Summarize key points, concerns, and next steps from these notes."},
                {"role": "user", "content": notes}
            ]
        )
        result = response.choices[0].message.content.strip()
        st.success(result)
        st.session_state["crm_result"] = result
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
            ws.append_row(["Timestamp", "Client", "Notes", "Insights"])

        ws.append_row([
            str(datetime.datetime.now()),
            name,
            notes,
            result
        ])
        st.info("✅ Saved to CRM Insights Sheet.")
    except Exception as e:
        st.warning(f"Google Sheets error: {e}")

    # Admin PDF Export
    if st.session_state.get("user_role", "guest") == "admin":
        if st.button("📄 Export to PDF", key="crm_pdf"):
            buffer = io.BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, "CRM Insight Report")
            c.drawString(100, 735, f"Client: {name}")
            c.drawString(100, 720, f"Notes: {notes[:90]}")
            c.drawString(100, 705, f"AI Insights: {result[:300]}")
            c.save()
            buffer.seek(0)
            st.download_button("Download PDF", buffer, file_name=f"{name}_insight_report.pdf")
