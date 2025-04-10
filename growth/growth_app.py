import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📈 Business Growth")
    st.markdown("### Explore new growth strategies and revenue ideas.")

    st.sidebar.header("💡 Growth Guide")
    st.sidebar.write("**What this tab does:** Provides growth tactics and business scaling advice.")
    st.sidebar.write("**What to enter:** Your business type, niche, stage of growth, or pain points.")
    st.sidebar.write("**How to use:** Use GPT’s output for lead gen, upselling, or expansion.")

    prompt = st.text_area("What growth ideas or challenges are you exploring?", key="growth_input")

    if st.button("Suggest a Growth Idea", key="growth_autofill"):
        prompt = "How can I scale my online consulting service to $10k/month?"

    if st.button("Run GPT-4o Autofill", key="growth_run") and prompt:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a startup mentor helping scale growth."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": prompt}, sheet_tab="Growth")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="growth_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Growth Report")
        c.drawString(100, 735, f"Input: {prompt}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="growth_report.pdf")
