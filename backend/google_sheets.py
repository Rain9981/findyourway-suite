import gspread
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

USERS_HEADERS = [
    "username",
    "password",
    "role",
    "status",
    "created_at",
    "created_by",
    "notes",
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
        return workbook.worksheet(sheet_tab)
    except gspread.exceptions.WorksheetNotFound:
        pass

    try:
        return workbook.add_worksheet(title=sheet_tab, rows=rows, cols=cols)
    except gspread.exceptions.APIError:
        for ws in workbook.worksheets():
            if ws.title.strip().lower() == sheet_tab.strip().lower():
                return ws
        raise


def save_data(role, data_dict, sheet_tab="General"):
    worksheet = get_or_create_worksheet(sheet_tab)

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

    if not current_values:
        worksheet.append_row(USERS_HEADERS)
    else:
        first_row = current_values[0]
        if all(str(cell).strip() == "" for cell in first_row):
            worksheet.update("A1:G1", [USERS_HEADERS])


def create_user_record(username, password, role, created_by="admin", notes=""):
    create_users_tab_if_missing()
    worksheet = get_or_create_worksheet("Users", rows="200", cols="10")

    row = [
        username.strip().lower(),
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


def save_all_user_records(users):
    """
    Rewrites the Users sheet with the provided list of user dicts.
    """
    create_users_tab_if_missing()
    worksheet = get_or_create_worksheet("Users", rows="500", cols="10")

    rows = [USERS_HEADERS]

    for user in users:
        rows.append([
            str(user.get("username", "")).strip().lower(),
            str(user.get("password", "")).strip(),
            str(user.get("role", "basic")).strip().lower(),
            str(user.get("status", "active")).strip().lower(),
            str(user.get("created_at", "")).strip(),
            str(user.get("created_by", "")).strip(),
            str(user.get("notes", "")).strip(),
        ])

    worksheet.clear()
    worksheet.update("A1:G" + str(len(rows)), rows)


def update_user_record(current_username, new_username=None, new_password=None, new_role=None, new_status=None, new_notes=None):
    """
    Updates one user record by username.
    Returns (success, message)
    """
    users = get_sheet_data("Users")
    current_username = current_username.strip().lower()

    if current_username in ["admin", "basic", "elite", "premium"]:
        return False, "Reserved backup logins cannot be edited here."

    target_index = None
    for i, user in enumerate(users):
        if str(user.get("username", "")).strip().lower() == current_username:
            target_index = i
            break

    if target_index is None:
        return False, "User not found."

    target_user = users[target_index]

    final_username = (new_username or target_user.get("username", "")).strip().lower()
    final_password = (new_password if new_password is not None and new_password != "" else target_user.get("password", "")).strip()
    final_role = (new_role or target_user.get("role", "basic")).strip().lower()
    final_status = (new_status or target_user.get("status", "active")).strip().lower()
    final_notes = target_user.get("notes", "") if new_notes is None else str(new_notes)

    if not final_username:
        return False, "Username cannot be blank."

    if final_username in ["admin", "basic", "elite", "premium"]:
        return False, "That username is reserved for backup logins."

    if final_role not in ["basic", "elite", "premium", "admin"]:
        return False, "Invalid role selected."

    if final_status not in ["active", "inactive"]:
        return False, "Invalid status selected."

    for i, user in enumerate(users):
        existing_username = str(user.get("username", "")).strip().lower()
        if i != target_index and existing_username == final_username:
            return False, "Another user already has that username."

    target_user["username"] = final_username
    target_user["password"] = final_password
    target_user["role"] = final_role
    target_user["status"] = final_status
    target_user["notes"] = final_notes

    save_all_user_records(users)
    return True, f"User '{final_username}' updated successfully."


def delete_user_record(username):
    """
    Deletes one user record by username.
    Returns (success, message)
    """
    users = get_sheet_data("Users")
    username = username.strip().lower()

    if username in ["admin", "basic", "elite", "premium"]:
        return False, "Reserved backup logins cannot be deleted here."

    new_users = [
        user for user in users
        if str(user.get("username", "")).strip().lower() != username
    ]

    if len(new_users) == len(users):
        return False, "User not found."

    save_all_user_records(new_users)
    return True, f"User '{username}' deleted successfully."