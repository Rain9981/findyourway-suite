    try:
        # Fix: Prevent error if the sheet already exists
        from gspread.exceptions import WorksheetNotFound
        import gspread
        import json
        import datetime
        from oauth2client.service_account import ServiceAccountCredentials

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = json.loads(st.secrets["google_sheets"]["service_account"])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

        try:
            worksheet = sheet.worksheet("Sentiment Analysis")
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="Sentiment Analysis", rows="100", cols="20")

        # Add headers if empty
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
