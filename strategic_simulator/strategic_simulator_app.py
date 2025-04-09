import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("AI Tool: " + __name__.replace("_", " ").title())
    st.markdown("### Use GPT-4o to assist your business strategy.")

    user_input = st.text_area("Enter prompt or info:", key=f"__main___input")

    if st.button("Run GPT Analysis", key=f"__main___run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful business AI assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab=__name__.replace("_", " ").title())
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export PDF", key=f"__main___pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Report: {__name__.replace('_',' ').title()}")
        y = 735
        for k, v in locals().items():
            if not k.startswith("_") and k != "client":
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")
