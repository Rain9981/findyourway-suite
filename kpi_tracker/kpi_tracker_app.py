import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📊 KPI Tracker")
    st.markdown("### Monitor your key business performance metrics.")

    st.sidebar.header("💡 KPI Tracker Guide")
    st.sidebar.write("**What this tab does:** Helps you define and refine the KPIs that matter to your business.")
    st.sidebar.write("**What to enter:** Describe the metrics you want to track or improve (e.g. 'customer churn rate' or 'monthly recurring revenue').")
    st.sidebar.write("**How to use:** Use GPT suggestions to refine your tracking strategy or define new KPIs.")

    user_input = st.text_area("Describe the KPIs you're tracking or struggling with:", key="kpi_tracker_input")

    if st.button("Run GPT-4o Autofill", key="kpi_tracker_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a KPI strategist helping businesses track performance effectively."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="KPI Tracker")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        if "already exists" in str(e):
            st.warning(f"✅ Sheet already exists, appending data.")
        else:
            st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="kpi_tracker_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "KPI Tracker Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="kpi_tracker_report.pdf")
