import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
import datetime

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🛠️ Operations Audit")
    st.markdown("### Improve your workflow, productivity, or systems.")

    st.sidebar.header("💡 Operations Audit Guide")
    st.sidebar.write("**What this tab does:** Reviews operational inefficiencies or team workflows.")
    st.sidebar.write("**What to enter:** A process, workflow, or performance issue.")
    st.sidebar.write("**How to use:** Get actionable GPT suggestions to streamline operations.")

    user_input = st.text_area("Describe an operations challenge or system to review:", key="operations_audit_input")

    if st.button("Run Operations Analysis", key="operations_audit_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an operations consultant. Diagnose inefficiencies and improve workflow."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
    save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Operations Audit")
    st.info("✅ Data saved to Google Sheets.")
except Exception as e:
    st.warning(f"Google Sheets not connected. Error: {e}")


    if st.button("Export to PDF", key="operations_audit_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Operations Audit Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="operations_audit_report.pdf")
