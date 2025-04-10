import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📣 Lead Generation")
    st.markdown("### Generate client attraction strategies using AI.")

    st.sidebar.header("💡 Lead Generation Guide")
    st.sidebar.write("**What this tab does:** Helps craft strategies for attracting potential leads.")
    st.sidebar.write("**What to enter:** Describe your offer, niche, or ideal customer.")
    st.sidebar.write("**How to use it:** Use AI output for outreach scripts, CTAs, or funnel planning.")

    example_prompt = "Create 3 ways to generate leads for a digital marketing agency targeting real estate agents."
    user_input = st.text_area("Describe your offer, niche, or lead-gen challenge:", value=example_prompt, key="lead_generation_input")

    if st.button("Generate Lead Ideas", key="lead_generation_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a lead generation expert helping small businesses attract leads."},
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
            sheet_tab="Lead Generation"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="lead_generation_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Lead Generation Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="lead_generation_report.pdf")
