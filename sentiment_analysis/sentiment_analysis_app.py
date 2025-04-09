import streamlit as st
import pandas as pd
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📊 Sentiment Analyzer")
    st.markdown("### Gauge public or client sentiment.")

    query = st.text_input("Enter topic or text")

    if st.button("Run GPT Analysis") and query:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )

        output = response.choices[0].message.content
        st.success(output)

        # Optional: save to Google Sheets
        try:
            from backend.google_sheets import save_data
            save_data(st.session_state.get("user_role", "guest"), {"query": query, "output": output})
            st.info("✅ Data saved to Google Sheets.")
        except Exception as e:
            st.warning("Google Sheets not connected.")
            st.text(str(e))

    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Consulting Report")
        c.drawString(100, 735, "------------------")
        y = 720
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")

