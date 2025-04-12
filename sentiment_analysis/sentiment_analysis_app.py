import streamlit as st
from openai import OpenAI
import io
import datetime
import json
import gspread
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("💬 Sentiment Analyzer")
    st.markdown("### Paste feedback or comments to analyze tone and sentiment.")

    st.sidebar.header("💡 Sentiment Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Analyzes positive, negative, or neutral sentiment in text.
    - **What to enter:** Customer feedback, reviews, or internal notes.
    - **How to use:** Paste input or use example, then run GPT-4o to get insights.
    """)

    default_prompt = "The customer said the service was slow, but they appreciated the staff’s kindness."

    if "sentiment_analysis_autofill_triggered" not in st.session_state:
        st.session_state["sentiment_analysis_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="sentiment_analysis_autofill"):
        st.session_state["sentiment_analysis_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["sentiment_analysis_autofill_triggered"] else ""

    user_input = st.text_area("Enter customer feedback:", value=input_value, key="sentiment_analysis_input")

    if st.button("🚀 Analyze with GPT-4o", key="sentiment_analysis_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a customer sentiment expert. Label tone as Positive, Neutral, or Negative, and explain."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.session_state["sentiment_analysis_result"] = response.choices[0].message.content.strip()
            st.success(st.session_state["sentiment_analysis_result"])
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Sentiment Analyzer")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Sentiment Analyzer", rows="100", cols="20")

        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input", "Sentiment Result"])

        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input,
            st.session_state.get("sentiment_analysis_result", "")
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("📄 Export to PDF", key="sentiment_analysis_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Sentiment Analysis Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.drawString(100, 720, f"Result: {st.session_state.get('sentiment_analysis_result', '')}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="sentiment_analysis_report.pdf")
