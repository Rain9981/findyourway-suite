import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📢 Marketing Hub")
    st.markdown("### Explore and refine marketing strategies using AI suggestions.")

    st.sidebar.header("💡 Marketing Hub Guide")
    st.sidebar.write("**What this tab does:** Helps design or optimize your marketing efforts.")
    st.sidebar.write("**What to input:** Describe your product, campaign, or ideal audience.")
    st.sidebar.write("**How to use it:** Use GPT to generate campaigns, channels, or brand ideas.")

    example_prompt = "Create a social media strategy for a skincare brand targeting Gen Z."
    user_input = st.text_area("Enter your marketing need or campaign goal:", value=example_prompt, key="marketing_hub_input")

    if st.button("Generate Marketing Plan", key="marketing_hub_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a marketing strategist helping businesses with campaign ideas, content, and outreach."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(
            st.session_state.get("user_role", "guest"),
            {"input": user_input},
            sheet_tab="Marketing Hub"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="marketing_hub_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Marketing Hub Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="marketing_hub_report.pdf")
