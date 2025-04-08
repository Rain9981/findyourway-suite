
import gspread
import streamlit as st
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials

def save_data(role, data_dict, sheet_tab="General"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    service_account_info = json.loads(st.secrets["google_sheets"]["service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

    try:
        worksheet = sheet.worksheet(sheet_tab)
    except:
        worksheet = sheet.add_worksheet(title=sheet_tab, rows="100", cols="20")

    row = [str(datetime.datetime.now()), role] + [str(v) for v in data_dict.values()]
    worksheet.append_row(row)

def save_dataframe(df, sheet_tab="Sentiment"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

    try:
        worksheet = sheet.worksheet(sheet_tab)
    except:
        worksheet = sheet.add_worksheet(title=sheet_tab, rows="100", cols="20")

    rows = [df.columns.tolist()] + df.astype(str).values.tolist()
    worksheet.append_rows(rows)
