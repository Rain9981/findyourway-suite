import streamlit as st
from openai import OpenAI
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from backend.google_sheets import save_data

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧩 Strategy Designer")
    st.markdown("### Map out business goals, obstacles, and tactics.")

    objective = st.text_input("Primary Business Objective")
    challenge = st.text_area("What are the biggest obstacles?")
    timeline = st.selectbox("Preferred Timeline", ["1-3 months", "3-6 months", "6-12 months", "1+ year"])

    st.sidebar.title("🧠 How to Use")
    st.sidebar.info("Describe the business goal and challenges. The AI will generate a strategic action plan.")

    if st.button("Generate Strategy"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategist helping clients plan effectively."},
                    {"role": "user", "content": f"Goal: {objective}\nChallenges: {challenge}\nTimeline: {timeline}"}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Strategy failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="StrategyDesigner")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        y = 750
        c.drawString(100, y, "Strategy Report")
        c.drawString(100, y-15, "------------------")
        for k, v in locals().items():
            if not k.startswith("_"):
                y -= 15
                c.drawString(100, y, f"{k}: {v}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="strategy_report.pdf")
