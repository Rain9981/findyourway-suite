import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🔗 Network Builder")
    st.markdown("### Strategize outreach and build key relationships.")

    st.sidebar.header("💡 Network Builder Guide")
    st.sidebar.write("**What this tab does:** Helps you brainstorm how to build strategic partnerships and grow your network.")
    st.sidebar.write("**What to enter:** Your niche, ideal partners, or collaboration goals.")
    st.sidebar.write("**How to use it:** Use GPT to uncover outreach strategies or pitch ideas.")

    example_prompt = "How can I build a referral network with fitness influencers?"
    user_input = st.text_area("Enter a networking challenge or goal:", value=example_prompt, key="network_builder_input")

    if st.button("Generate Outreach Strategy", key="network_builder_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're an expert in strategic networking and outreach."},
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
            sheet_tab="Network Builder"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="network_builder_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Network Builder Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_builder_report.pdf")
