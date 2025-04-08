import streamlit as st
import pandas as pd

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def run():
    st.title("📇 CRM Manager")
    st.markdown("### Track and manage clients.")

    client = st.text_input("Client Name")
    email = st.text_input("Email")
    stage = st.selectbox("Stage", ['Lead', 'Prospect', 'Customer'])

    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals())
        st.info("✅ Data saved to Google Sheets.")
    except:
        st.warning("Google Sheets not connected.")

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
