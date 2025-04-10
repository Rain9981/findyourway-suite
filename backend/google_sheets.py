import gspread
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def save_data(role, data_dict, sheet_tab="General"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

    try:
        worksheet = sheet.worksheet(sheet_tab)
    except:
        worksheet = sheet.add_worksheet(title=sheet_tab, rows="100", cols="20")

    # Write headers if sheet is new or empty
    if not worksheet.get_all_values():
        headers = ["Timestamp", "Role"] + list(data_dict.keys())
        worksheet.append_row(headers)

    # Append data
    row = [str(datetime.datetime.now()), role] + [str(v) for v in data_dict.values()]
    worksheet.append_row(row)
