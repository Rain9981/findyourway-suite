import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📈 Business Development")
    st.markdown("### Unlock strategies to grow partnerships, revenue, and market reach.")

    # Sidebar Consulting Guide
    st.sidebar.header("💼 Business Development Guide")
    st.sidebar.write("**What this tab does:** Helps uncover sales strategies, expansion plans, and growth tactics.")
    st.sidebar.write("**What to enter:** A question or topic about scaling your business, sales, or partnerships.")
    st.sidebar.write("**How to use it:** Review GPT’s advice to build out development plans, outreach funnels, or partnership models.")

    # Input prompt tailored to business development
    user_input = st.text_area("What do you need help with? (e.g., How can I grow my client base using strategic partnerships?)", key="business_development_input")
    if st.button("✨ Autofill Suggestion", key="business_development_fill"):
        user_input = "Suggest something for business development"


    if st.button("Run GPT-4o Autofill", key="business_development_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategist helping improve sales, growth, and development pipelines."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    # Save to Google Sheets
    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Business Development")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    # PDF Export
    if st.button("Export to PDF", key="business_development_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Business Development Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="business_development_report.pdf")
