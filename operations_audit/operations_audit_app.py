import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("⚙️ Operations Audit")

    st.sidebar.header("💡 Operations Audit Guide")
    st.sidebar.markdown("""
    **What this tab does:**  
    Reviews your internal systems, workflows, and bottlenecks using AI.

    **What to input:**  
    Describe an area of your business operations you'd like to assess or improve.

    **How to use:**  
    Use GPT suggestions to optimize tasks, boost efficiency, or cut costs.
    """)

    user_input = st.text_area(
        "Describe an operational process or area you'd like to audit:",
        key="operations_audit_input"
    )

    if st.button("💬 Run GPT Audit", key="operations_audit_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an operations consultant evaluating internal processes for optimization."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    if st.button("✨ Autofill Sample Prompt", key="operations_audit_suggest"):
        st.session_state["operations_audit_input"] = "Our client onboarding process takes too long. How can we improve it?"

    try:
        save_data(
            st.session_state.get("user_role", "guest"),
            {"input": user_input},
            sheet_tab="Operations Audit"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="operations_audit_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Operations Audit Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="operations_audit_report.pdf")
