from backend.google_sheets import get_sheet_data

def authenticate_user(username, password):
    try:
        users = get_sheet_data("Users")
    except Exception:
        return False, None

    username = str(username).strip().lower()
    password = str(password).strip()

    for user in users:
        sheet_username = str(user.get("username", "")).strip().lower()

        # Support both old and new header names
        sheet_password = str(
            user.get("password", user.get("password_hash", ""))
        ).strip()

        sheet_role = str(user.get("role", "")).strip().lower()
        sheet_status = str(user.get("status", "active")).strip().lower()

        if sheet_username == username:
            if sheet_status != "active":
                return False, None

            if sheet_password == password:
                return True, sheet_role

            return False, None

    return False, None