import streamlit as st
import datetime
import json
import io
import gspread
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    st.title("📣 Marketing Hub")
    st.markdown("Refine your campaign ideas and brand messaging.")

    st.sidebar.header("💡 Marketing Strategy Tips")
    st.sidebar.markdown("""
    - Describe your product, audience, or campaign.
    - GPT will give creative direction or messaging ideas.
    - Save results or export as PDF.
    """)

    default_prompt = "We're launching a natural skincare line and need content ideas for Instagram and email."

    if "marketing_hub_autofill_triggered" not in st.session_state:
        st.session_state["marketing_hub_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="marketing_hub_autofill"):
        st.session_state["marketing_hub_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["marketing_hub_autofill_triggered"] else ""

    user_input = st.text_area("Describe your product and goal:", value=input_value, key="marketing_hub_input")

    if st.button("🚀 Run GPT-4o Strategy", key="marketing_hub_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a brand marketing strategist. Give campaign ideas and brand messaging tips."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["marketing_hub_result"] = result
            st.subheader("📊 GPT-Generated Marketing Plan")
            st.success(result)

            # Save to Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Marketing Hub")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Marketing Hub", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "Marketing Plan"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")

            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="marketing_hub_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Marketing Hub Output")
                    c.drawString(100, 730, f"Input: {user_input[:90]}")
                    text = c.beginText(100, 710)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="marketing_plan.pdf")
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")
