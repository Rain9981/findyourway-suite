# ✅ 1. brand_positioning_app.py
import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🗭 Brand Positioning")
    st.markdown("### Define your market identity and positioning.")

    st.sidebar.header("💡 Brand Positioning Guide")
    st.sidebar.write("**What this tab does:** Helps define your brand's unique position in the market.")
    st.sidebar.write("**What to enter:** A description of your business, industry, or audience.")
    st.sidebar.write("**How to use it:** Use the GPT-generated insight to build taglines, messaging, or customer profiles.")

    user_input = st.text_area("What do you want help with? (e.g., Define my brand for health-conscious Gen Z)", key="brand_positioning_input")
    if st.button("✨ Autofill Suggestion", key="brand_positioning_fill"):
        user_input = "Suggest something for brand positioning"


    if st.button("Run GPT-4o Autofill", key="brand_positioning_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a branding expert helping define market positioning."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Brand Positioning")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="brand_positioning_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Brand Positioning Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="brand_positioning_report.pdf")
