import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

def run():
    st.title("operations audit".title() + " Tool")
    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.markdown("**What this tab does:** Analyzes your 'operations audit' strategy with AI.")
    st.sidebar.markdown("**What to input:** Enter a question, scenario, or business insight.")
    st.sidebar.markdown("**What you get:** Smart suggestions, plus export + Sheets saving.")

    prompt = st.text_area("💬 GPT prompt for operations audit", key="operations_audit_input")
    if st.button("✨ Autofill Suggestion", key="operations_audit_fill"):
        user_input = "Suggest something for operations audit"


    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    if st.button("Run GPT Analysis", key="operations_audit_run") and prompt:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a consulting AI specializing in operations audit."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": prompt}, sheet_tab="operations audit")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="operations_audit_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "GPT Analysis for operations audit")
        c.drawString(100, 735, f"Prompt: {prompt}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="operations_audit_report.pdf")
