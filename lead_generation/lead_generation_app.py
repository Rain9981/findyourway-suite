def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    st.title("🎯 Lead Generation")
    st.markdown("Generate lead magnet ideas and outreach strategies.")

    st.sidebar.header("💡 Lead Gen Guide")
    st.sidebar.markdown("""
    - Describe who you're trying to reach and what you're offering.
    - GPT will suggest lead magnets or strategies to grow your list.
    """)

    default_prompt = "We offer a business tax course and want to collect leads through a downloadable checklist."

    if "lead_gen_autofill_triggered" not in st.session_state:
        st.session_state["lead_gen_autofill_triggered"] = False

    if st.button("✨ Autofill Example", key="lead_gen_autofill"):
        st.session_state["lead_gen_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["lead_gen_autofill_triggered"] else ""

    user_input = st.text_area("Describe your audience and lead goal:", value=input_value, key="lead_gen_input")

    if st.button("🚀 Run GPT-4o Idea", key="lead_gen_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a lead generation expert. Suggest creative ways to collect leads."},
                    {"role": "user", "content": user_input}
                ]
            )
            result = response.choices[0].message.content.strip()
            st.session_state["lead_gen_result"] = result
            st.subheader("📋 GPT-Generated Lead Strategy")
            st.success(result)

            # Sheets + PDF
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = json.loads(st.secrets["google_sheets"]["service_account"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
            gs_client = gspread.authorize(credentials)
            sheet = gs_client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
            try:
                ws = sheet.worksheet("Lead Generation")
            except WorksheetNotFound:
                ws = sheet.add_worksheet(title="Lead Generation", rows="100", cols="20")
                ws.append_row(["Timestamp", "User Role", "Input", "Result"])
            ws.append_row([
                str(datetime.datetime.now()),
                st.session_state.get("user_role", "guest"),
                user_input,
                result
            ])
            st.info("✅ Saved to Google Sheets.")

            if st.session_state.get("user_role", "guest") == "admin":
                if st.button("📄 Export to PDF", key="lead_gen_pdf"):
                    buffer = io.BytesIO()
                    c = pdf_canvas.Canvas(buffer, pagesize=letter)
                    c.drawString(100, 750, "Lead Generation Report")
                    c.drawString(100, 730, f"Input: {user_input[:80]}")
                    c.drawString(100, 710, "GPT Result:")
                    text = c.beginText(100, 695)
                    for line in result.splitlines():
                        text.textLine(line[:100])
                    c.drawText(text)
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download PDF", buffer, file_name="lead_generation.pdf")
        except Exception as e:
            st.error(f"❌ Error: {e}")
