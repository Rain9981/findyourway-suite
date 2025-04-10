import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📊 KPI Tracker")

    st.sidebar.header("💡 KPI Tracker Guide")
    st.sidebar.markdown("""
    **What this tab does:**  
    Helps you track Key Performance Indicators (KPIs) and optimize metrics.

    **What to input:**  
    List KPIs you're tracking (sales, churn rate, engagement, etc.) or areas you'd like to improve.

    **How to use:**  
    GPT can recommend benchmarks, insights, or ways to reach targets.
    """)

    user_input = st.text_area(
        "Describe the KPIs you're tracking or struggling with:",
        key="kpi_tracker_input"
    )

    if st.button("📈 Analyze KPIs", key="kpi_tracker_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a KPI expert helping optimize business performance metrics."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    if st.button("✨ Autofill Sample Prompt", key="kpi_tracker_suggest"):
        st.session_state["kpi_tracker_input"] = "Our sales KPIs are below target. How can we improve performance next quarter?"

    try:
        save_data(
            st.session_state.get("user_role", "guest"),
            {"input": user_input},
            sheet_tab="KPI Tracker"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="kpi_tracker_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "KPI Tracker Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="kpi_tracker_report.pdf")
