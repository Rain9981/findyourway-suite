from backend.google_sheets import get_sheet_data

def authenticate_user(username, password):
    try:
        users = get_sheet_data("Users")
    except:
        return False, None

    username = username.lower().strip()

    for user in users:
        if user.get("username", "").lower() == username:
            if user.get("status") != "active":
                return False, None

            if user.get("password") == password:
                return True, user.get("role")

    return False, None