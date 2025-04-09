import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

def run():
    st.title("crm manager".title() + " Tool")
    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.markdown("**What this tab does:** Analyzes your 'crm manager' strategy with AI.")
    st.sidebar.markdown("**What to input:** Enter a question, scenario, or business insight.")
    st.sidebar.markdown("**What you get:** Smart suggestions, plus export + Sheets saving.")

    prompt = st.text_area("💬 GPT prompt for crm manager", key="crm_manager_input")

    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    if st.button("Run GPT Analysis", key="crm_manager_run") and prompt:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a consulting AI specializing in crm manager."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": prompt}, sheet_tab="crm manager")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="crm_manager_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "GPT Analysis for crm manager")
        c.drawString(100, 735, f"Prompt: {prompt}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="crm_manager_report.pdf")
