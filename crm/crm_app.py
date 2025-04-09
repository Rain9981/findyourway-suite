import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("AI Tool: " + "crm".replace("_", " ").title())
    st.markdown("### Use GPT-4o to enhance your strategy or operations.")
    user_input = st.text_area("Enter prompt or info:", key="crm_input")

    if st.button("Run GPT Analysis", key="crm_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful business consultant."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="crm".replace("_", " ").title())
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="crm_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Report: crm".replace("_", " ").title())
        y = 735
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")

    # 🧭 Sidebar consulting insights
    with st.sidebar:
        st.markdown("## 💡 Guide")
        st.write(f"This tab helps analyze or build insights for **{'crm'.replace('_', ' ').title()}**.")
        st.markdown("- Provide a clear question or topic.")
        st.markdown("- Click **Run GPT Analysis** to see suggestions.")
        st.markdown("- Export results or save to your Sheets.")
