import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def save_sentiment_data(df):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["google_sheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(creds_dict["sheet_id"]).sheet1

    rows = [df.columns.tolist()] + df.values.tolist()
    sheet.append_rows(rows)
