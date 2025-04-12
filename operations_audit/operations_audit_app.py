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
    st.title("⚙️ Operations Audit")
    st.markdown("Evaluate and streamline your current business processes.")

    st.sidebar.header("💡 Audit Guide")
    st.sidebar.markdown("""
    - Describe a workflow or operational issue.
    - GPT will suggest ways to improve, automate, or systematize it.
    - Export if you need to present changes.
    """)

    default_prompt = "Our onboarding process is slow and uses 4 tools. How can we streamline it?"

    if "ops_audit_autofill_triggered" not in st.session_state:
        st.session_state["ops_audit_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="ops_audit_autofill"):
        st.session_state["ops_audit_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["ops_audit_autofill_triggered"] else ""

    user_input = st.text_area("Describe your operational workflow or bottleneck:", value=input_value, key="ops_audit_input")

    if st.button("🚀 Analyze with GPT-4o", key="ops_audit_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're an operations consultant improving internal processes."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["ops_audit_result"] = result
            st.subheader("🛠️ GPT-Generated Operations Suggestions")
            st.success(result)

            # Save to Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Operations Audit")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Operations Audit", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "GPT Result"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")

            # PDF export
            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="ops_audit_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Operations Audit")
                    c.drawString(100, 730, f"Input: {user_input[:90]}")
                    text = c.beginText(100, 710)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="operations_audit.pdf")
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")
