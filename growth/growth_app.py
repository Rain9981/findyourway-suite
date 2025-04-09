import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

TAB_LABEL = "growth".replace("_", " ").title()

def run():
    st.title("AI Tool: " + TAB_LABEL)
    st.markdown("### Use GPT-4o to assist your business strategy.")

    # Smart Input Prompt
    prompt_label = {
        "brand_positioning": "Describe your brand and audience",
        "business_development": "Describe your current growth plan",
        "lead_generation": "What product/service are you selling?",
        "strategy_designer": "What goal or outcome are you designing for?",
        "forecasting": "Enter data trends, dates, or sales info",
        "sentiment_analysis": "Enter customer or public comments",
        "strategic_simulator": "Describe your strategy scenario",
        "marketing_hub": "What are your marketing goals?",
        "crm_dashboard": "Enter client notes, stages, or updates",
    }.get("growth", "Enter prompt or info:")

    user_input = st.text_area(prompt_label, key=f"{tab}_input")

    # GPT Autofill
    if st.button("Run GPT Analysis", key=f"{tab}_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a business consultant helping with {TAB_LABEL}"},
                    {"role": "user", "content": user_input},
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab=TAB_LABEL)
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key=f"{tab}_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Consulting Report")
        y = 735
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")

    # Sidebar Guide
    with st.sidebar:
        st.subheader("💡 Guide")
        st.markdown(f"**This tab:** {TAB_LABEL}")
        st.markdown("- What to enter: A specific question or scenario")
        st.markdown("- What this helps you do: Generate insights")
        st.markdown("- How to interpret: Use suggestions as action steps")
