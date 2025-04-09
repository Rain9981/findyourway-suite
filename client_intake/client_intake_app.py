import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("client_intake".replace("_", " ").title())

    # Sidebar consulting guide
    with st.sidebar:
        st.header("📌 Guide")
        st.markdown("**Input Advice:** Enter a clear business prompt.\n\n**Tool Purpose:** GPT-powered insights, PDF export, and auto Google Sheets saving.\n\n**Consulting Tip:** Use this tab to quickly evaluate or simulate strategies.")

    user_input = st.text_area("Enter prompt or info:")

    if st.button("Run GPT-4o Analysis") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful AI consultant."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="client_intake")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"⚠️ Google Sheets not connected: {e}")

    if st.button("Export PDF"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Consulting Report")
        y = 735
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")
