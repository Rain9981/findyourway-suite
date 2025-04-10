import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🌐 Network Expansion")

    st.sidebar.header("💡 Network Builder Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you brainstorm how to grow and strengthen your business network.
    - **What to input:** Describe your current network, growth goals, or outreach ideas.
    - **How to use:** Use the suggestions to build collaborations, partnerships, or outreach campaigns.
    """)

    user_input = st.text_area("Describe your network growth goal (e.g., Find more B2B partners in health tech):", key="network_input")

    if st.button("Run GPT-4o Autofill", key="network_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a networking strategist helping expand professional influence."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Network")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="network_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Network Expansion Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_report.pdf")
