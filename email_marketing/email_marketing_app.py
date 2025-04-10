import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📨 Email Marketing")
    st.markdown("### Create engaging emails and campaigns with AI.")

    st.sidebar.header("💡 Email Marketing Guide")
    st.sidebar.write("**What this tab does:** Helps you create email campaigns, subject lines, and follow-ups.")
    st.sidebar.write("**What to enter:** Describe the email topic, audience, and tone.")
    st.sidebar.write("**How to use:** Use the generated email as-is or edit before sending.")

    prompt = st.text_area("Describe your email goal (e.g. 'Launch announcement to existing customers')", key="email_marketing_input")

    if st.button("✍️ Autofill Email Prompt", key="email_marketing_autofill"):
        prompt = "Write a warm promotional email to welcome new subscribers to a business newsletter."

    if st.button("Run GPT Email Writer", key="email_marketing_run") and prompt:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a world-class email copywriter."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": prompt}, sheet_tab="email marketing")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="email_marketing_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Email Marketing Report")
        c.drawString(100, 735, f"Input: {prompt}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="email_marketing_report.pdf")
