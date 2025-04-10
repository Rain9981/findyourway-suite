import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🚨 Oops Audit")

    st.sidebar.header("💡 Oops Audit Guide")
    st.sidebar.markdown("""
    **What this tab does:**  
    Helps identify business mistakes and turn them into strategic lessons.

    **What to input:**  
    Describe a business misstep, missed opportunity, or failed campaign.

    **How to use:**  
    Use GPT insights to recover, pivot, or improve future decision-making.
    """)

    user_input = st.text_area(
        "Describe a business mistake, failure, or challenge to review:",
        key="oops_audit_input"
    )

    if st.button("💬 Run GPT Audit", key="oops_audit_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business coach analyzing failures and suggesting recovery strategies."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    if st.button("✨ Autofill Sample Prompt", key="oops_audit_suggest"):
        st.session_state["oops_audit_input"] = "We launched a product with no market research and got low engagement. What could we have done better?"

    try:
        save_data(
            st.session_state.get("user_role", "guest"),
            {"input": user_input},
            sheet_tab="Oops Audit"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="oops_audit_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Oops Audit Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="oops_audit_report.pdf")
