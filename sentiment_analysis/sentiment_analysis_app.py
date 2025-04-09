import streamlit as st
import pandas as pd
import openai
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from openai import OpenAI

# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📊 Sentiment Analyzer")
    st.markdown("### Gauge public or client sentiment using GPT-4.")

    query = st.text_area("Enter topic or text", height=150)

    if st.button("Run GPT Analysis") and query.strip():
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful business sentiment analysis expert."},
                    {"role": "user", "content": query}
                ]
            )
            output = response.choices[0].message.content
            st.success(output)

            # Save to Google Sheets
            try:
                from backend.google_sheets import save_data
                save_data(st.session_state.get("user_role", "guest"), {
                    "query": query,
                    "response": output
                }, sheet_tab="Sentiment")
                st.info("✅ Data saved to Google Sheets.")
            except Exception as e:
                st.warning("Google Sheets not connected.")
                st.text(str(e))

        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    # Export to PDF
    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Sentiment Analysis Report")
        c.drawString(100, 735, "----------------------------")
        y = 720
        if query:
            c.drawString(100, y, f"Query: {query[:80]}...")
            y -= 20
        if 'output' in locals():
            c.drawString(100, y, "Response:")
            y -= 15
            for line in output.split('\n'):
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(100, y, line[:100])
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="sentiment_report.pdf")
