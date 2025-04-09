import streamlit as st
import pandas as pd

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def run():
    st.title("📈 Revenue Forecasting")
    st.markdown("### Project revenue growth.")

    business_name = st.text_input("Business Name")
    revenue = st.number_input("Starting Revenue", min_value=0, value=1000, step=1)
    growth = st.slider("Growth %", min_value=0, max_value=100, value=10)

    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="Forecasting")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")



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
