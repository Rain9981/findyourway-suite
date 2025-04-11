import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🌱 Self Enhancement")
    st.markdown("### Explore ways to grow your personal and professional self.")

    st.sidebar.header("💡 Self Enhancement Guide")
    st.sidebar.write("**What this tab does:** Suggests ideas for personal growth and self-improvement.")
    st.sidebar.write("**What to enter:** Goals, habits, mindset shifts, or growth challenges.")
    st.sidebar.write("**How to use:** Use GPT to brainstorm self-enhancement plans.")

    user_input = st.text_area("What aspect of your personal or professional self are you improving?", key="self_enhancement_input")

    if st.button("Suggest Growth Plan", key="self_enhancement_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a coach helping someone build their personal and professional growth."},
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
            sheet_tab="Self Enhancement"
        )
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
