import streamlit as st
import pandas as pd
import openai
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

openai.api_key = st.secrets['openai']['api_key']

def run():
    st.title("📐 Strategy Designer")
    st.markdown("### Draft your business strategy.")

    plan = st.text_area("Write your strategic plan")

    if st.button("Run GPT Analysis"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze the following input: "},
                {"role": "user", "content": business_name if 'business_name' in locals() else 'N/A'}
            ]
        )
        st.success(response['choices'][0]['message']['content'].strip())

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
