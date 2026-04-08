import gspread
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def get_gsheet_client():
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, SCOPE)
    return gspread.authorize(credentials)

def get_workbook():
    client = get_gsheet_client()
    return client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

def get_or_create_worksheet(sheet_tab="General", rows="100", cols="20"):
    workbook = get_workbook()
    try:
        worksheet = workbook.worksheet(sheet_tab)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = workbook.add_worksheet(title=sheet_tab, rows=rows, cols=cols)
    return worksheet

def save_data(role, data_dict, sheet_tab="General"):
    worksheet = get_or_create_worksheet(sheet_tab)

    # Add headers only if the worksheet is empty
    if not worksheet.get_all_values():
        headers = ["Timestamp", "Role"] + list(data_dict.keys())
        worksheet.append_row(headers)

    row = [str(datetime.datetime.now()), role] + [str(v) for v in data_dict.values()]
    worksheet.append_row(row)

def get_sheet_data(sheet_tab="Users"):
    """
    Safely reads a worksheet and returns list of dicts.
    Returns [] if anything goes wrong so backup logins still work.
    """
    try:
        worksheet = get_or_create_worksheet(sheet_tab)
        records = worksheet.get_all_records()
        return records if records else []
    except Exception as e:
        print(f"Google Sheets read failed for tab '{sheet_tab}': {e}")
        return []

def create_users_tab_if_missing():
    """
    Ensures the Users tab exists with the exact header row needed.
    """
    worksheet = get_or_create_worksheet("Users", rows="200", cols="10")
    current_values = worksheet.get_all_values()

    expected_headers = [
        "username",
        "password",
        "role",
        "status",
        "created_at",
        "created_by",
        "notes",
    ]

    if not current_values:
        worksheet.append_row(expected_headers)
    else:
        first_row = current_values[0]
        if first_row != expected_headers:
            # Only set headers if the sheet looks empty except for formatting
            if len(current_values) == 0 or all(cell == "" for cell in first_row):
                worksheet.update("A1:G1", [expected_headers])

def create_user_record(username, password, role, created_by="admin", notes=""):
    """
    Adds a user directly to the Users tab without the Timestamp/Role wrapper.
    """
    create_users_tab_if_missing()
    worksheet = get_or_create_worksheet("Users", rows="200", cols="10")

    row = [
        username.strip(),
        password.strip(),
        role.strip().lower(),
        "active",
        str(datetime.datetime.now()),
        created_by,
        notes,
    ]
    worksheet.append_row(row)

def username_exists(username):
    users = get_sheet_data("Users")
    username = username.strip().lower()
    for user in users:
        if str(user.get("username", "")).strip().lower() == username:
            return True
    return False