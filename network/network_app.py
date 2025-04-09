import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("AI Tool: " + "network".replace("_", " ").title())
    st.markdown("### Use GPT-4o to assist your business strategy.")

    user_input = st.text_area("Enter prompt or info:", key=f"{tab}_input")

    if st.button("Run GPT Analysis", key=f"{tab}_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategy assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="network")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key=f"{tab}_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        y = 750
        c.drawString(100, y, f"Report: {tab.replace('_', ' ').title()}")
        y -= 20
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name=f"{tab}_report.pdf")

    # Sidebar guide
    with st.sidebar:
        st.markdown("## 🧠 Consulting Insights")
        st.info(f"Use this tool to analyze and improve your business's {tab.replace('_', ' ')}. Ideal input: pain points, questions, or data insights.")
