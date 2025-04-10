import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧠 Strategy Designer")
    st.markdown("### Craft business strategies using GPT insight.")

    st.sidebar.header("💡 Strategy Designer Guide")
    st.sidebar.write("**What this tab does:** Helps you define and design growth strategies.")
    st.sidebar.write("**What to enter:** Business scenario, goals, or market challenges.")
    st.sidebar.write("**How to use it:** Use suggestions to plan your strategic moves.")

    example_prompt = "Design a strategy to expand into new markets for a SaaS platform."
    user_input = st.text_area("Enter a strategic question or idea:", value=example_prompt, key="strategy_designer_input")

    if st.button("Generate Strategy", key="strategy_designer_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a business strategist helping users design scalable growth strategies."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Strategy Designer")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="strategy_designer_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Strategy Designer Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="strategy_designer_report.pdf")
