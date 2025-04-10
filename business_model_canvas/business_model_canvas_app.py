import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📐 Business Model Canvas")
    st.markdown("### Draft or enhance your business model.")

    st.sidebar.header("💡 Business Model Guide")
    st.sidebar.write("**What this tab does:** Helps map out your business using canvas logic.")
    st.sidebar.write("**What to enter:** Describe your idea, partners, customers, or key value.")
    st.sidebar.write("**How to use it:** Use GPT-4o to draft your canvas or refine it for presentations.")

    user_input = st.text_area("What aspect of your business model needs help?", key="business_model_canvas_input")
    if st.button("✨ Autofill Suggestion", key="business_model_canvas_fill"):
        user_input = "Suggest something for business model canvas"


    if st.button("Run GPT-4o Autofill", key="business_model_canvas_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're an expert at crafting business model canvases."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Business Model Canvas")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="business_model_canvas_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Business Model Canvas Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="business_model_canvas_report.pdf")
