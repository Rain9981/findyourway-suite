import streamlit as st
import pandas as pd
from openai import OpenAI
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧠 Strategic Simulator")
    st.markdown("### Test strategy scenarios using GPT-4o.")

    scenario = st.text_area("Describe your business strategy or scenario")

    if st.button("Run Strategy Simulation") and scenario:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategy simulator."},
                    {"role": "user", "content": scenario}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Simulation failed: {e}")

    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="Simulator")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Strategic Simulation Report")
        y = 735
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="strategy_report.pdf")
