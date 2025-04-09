import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("AI Tool: Business Development")
    prompt_label = "What would you like help with regarding Business Development?"
    st.sidebar.header("💡 Guide")
    st.sidebar.write("**This tab helps you:**")
    st.sidebar.write("- Uncover partnerships, new markets, and sales strategies.")
    st.sidebar.write("- Use GPT-4o to enhance decision-making.")
    st.sidebar.write("- Save to Sheets or export a PDF.")

    user_input = st.text_area(prompt_label, key="business_development_input")

    if st.button("Run GPT Analysis", key="business_development_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Business Development."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Business Development")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="business_development_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Consulting Report - Business Development")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="business_development_report.pdf")

