import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("AI-Enhanced Tool: " + "business_development".replace("_", " ").title())
    st.markdown("### Use GPT-4o to generate insights.")

    user_input = st.text_area("Enter your business question or topic:")

    if st.button("Run GPT Analysis") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business consultant."},
                    {"role": "user", "content": user_input}
                ]
            )
            output = response.choices[0].message.content.strip()
            st.success(output)
        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="business_development".title().replace("_", " "))
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Consulting Report")
        y = 735
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")

    with st.sidebar:
        st.markdown("### How to Use This Tab")
        st.info("""
        - Enter a topic/question related to business strategy.
        - Click **Run GPT Analysis** to generate expert-level insights.
        - Click **Export** to download the results or auto-save to Google Sheets.
        - Insights vary by tier: Basic, Elite, Admin.
        """)
