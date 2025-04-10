import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🎯 Strategic Canvas")
    st.markdown("### Visualize your unique market positioning.")

    st.sidebar.header("💡 Strategic Canvas Guide")
    st.sidebar.write("**What this tab does:** Helps you compare your business against competitors.")
    st.sidebar.write("**What to enter:** Describe your value curve, strengths, or what sets you apart.")
    st.sidebar.write("**How to use it:** Use GPT-4o to generate a strategic comparison of your value dimensions.")

    user_input = st.text_area("What market or competitors are you comparing?", key="canvas_input")
    if st.button("✨ Autofill Suggestion", key="canvas_fill"):
        user_input = "Suggest something for canvas"


    if st.button("Run GPT-4o Autofill", key="canvas_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a strategic consultant helping a business map out a competitive canvas."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Canvas")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="canvas_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Strategic Canvas Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="canvas_report.pdf")
