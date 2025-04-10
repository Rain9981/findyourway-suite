import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📝 Client Intake")
    st.markdown("### Collect and analyze new client information.")

    st.sidebar.header("💡 Intake Guide")
    st.sidebar.write("**What this tab does:** Helps you gather client background for onboarding.")
    st.sidebar.write("**What to enter:** Business name, industry, goals, pain points.")
    st.sidebar.write("**How to use it:** Store all intake data and use GPT to auto-summarize.")

    user_input = st.text_area("Enter new client background or notes", key="client_intake_input")

    if st.button("Summarize Intake", key="client_intake_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a consultant analyzing new client intake forms."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Client Intake")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="client_intake_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Client Intake Summary")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="client_intake_summary.pdf")
