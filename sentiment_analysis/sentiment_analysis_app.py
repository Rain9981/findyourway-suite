import streamlit as st
from openai import OpenAI
import io
import datetime
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧠 Sentiment Analysis")
    st.markdown("### Analyze customer tone, reviews, or feedback.")

    st.sidebar.header("💡 Sentiment Analysis Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Helps you understand the emotional tone of text.
    - **What to input:** Paste reviews, emails, or social media posts.
    - **How to use:** Use results to adjust marketing or customer service.
    """)

    user_input = st.text_area("Paste feedback, review, or customer text:", key="sentiment_analysis_input")

    if st.button("Run Sentiment Analysis", key="sentiment_analysis_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You analyze customer feedback and detect sentiment (positive, negative, neutral)."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        from gspread.exceptions import WorksheetNotFound
        import gspread
        import json
        from oauth2client.service_account import ServiceAccountCredentials

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client_gsheets = gspread.authorize(credentials)
        sheet = client_gsheets.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("sentiment analysis")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="sentiment analysis", rows="100", cols="20")

        if not worksheet.get_all_values():
            worksheet.append_row(["Timestamp", "User Role", "Input"])

        worksheet.append_row([
            str(datetime.datetime.now()),
            st.session_state.get("user_role", "guest"),
            user_input
        ])
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="sentiment_analysis_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Sentiment Analysis Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="sentiment_analysis_report.pdf")
