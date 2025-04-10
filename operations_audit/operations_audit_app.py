import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("⚙️ Operations Audit")
    st.markdown("### Review systems, processes, or bottlenecks.")

    st.sidebar.header("💡 Operations Audit Guide")
    st.sidebar.write("**What this tab does:** Helps uncover inefficiencies or process flaws.")
    st.sidebar.write("**What to enter:** Describe a workflow, system, or department.")
    st.sidebar.write("**How to use it:** Get suggestions for process improvements or audits.")

    user_input = st.text_area("What operational process would you like to evaluate?", key="operations_audit_input")

    if st.button("Audit Operations", key="operations_audit_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business operations expert identifying workflow problems and improvements."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(
            st.session_state.get("user_role", "guest"),
            {"input": user_input},
            sheet_tab="Operations Audit"
        )
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
