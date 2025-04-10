import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📈 Business Forecasting")
    st.markdown("### Use AI to project future trends, sales, or market growth.")

    st.sidebar.header("💡 Forecasting Guide")
    st.sidebar.write("**What this tab does:** Projects revenue, growth, or customer base.")
    st.sidebar.write("**What to enter:** Product/service, time frame, market trends.")
    st.sidebar.write("**How to use it:** Use GPT insights to guide budgeting or strategy.")

    user_input = st.text_area("What would you like to forecast? (e.g., Project revenue for next 6 months based on current growth)", key="forecasting_input")
    if st.button("✨ Autofill Suggestion", key="forecasting_fill"):
        user_input = "Suggest something for forecasting"


    if st.button("Run Forecast", key="forecasting_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business analyst skilled at forecasting."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"forecast_input": user_input}, sheet_tab="Forecasting")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export Forecast PDF", key="forecasting_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Forecast Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="forecast_report.pdf")
