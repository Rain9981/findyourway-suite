import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
import datetime

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧘 Self-Enhancement")
    st.markdown("### Improve your mindset, habits, or leadership skills.")

    st.sidebar.header("💡 Self-Enhancement Guide")
    st.sidebar.write("**What this tab does:** Helps boost mindset, leadership, or productivity.")
    st.sidebar.write("**What to enter:** Describe a challenge, habit, or leadership goal.")
    st.sidebar.write("**How to use:** Use the advice to build better business discipline or mindset.")

    user_input = st.text_area("Describe your self-growth challenge or goal:", key="self_enhancement_input")

    if st.button("Get Personal Growth Insight", key="self_enhancement_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a mindset coach helping entrepreneurs grow personally."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="self enhancement")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="self_enhancement_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Self Enhancement Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="self_enhancement_report.pdf")
