import streamlit as st
from backend.google_sheets import (
    create_user_record,
    create_users_tab_if_missing,
    get_sheet_data,
    username_exists,
)

def run():
    st.title("Admin User Manager")

    if st.session_state.get("user_role") != "admin":
        st.error("Admin access only")
        st.stop()

    create_users_tab_if_missing()

    st.subheader("Create New User")

    with st.form("create_user_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["basic", "elite", "premium", "admin"])
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Create User")

        if submitted:
            username_clean = username.strip().lower()
            password_clean = password.strip()

            if not username_clean:
                st.error("Username is required.")
            elif not password_clean:
                st.error("Password is required.")
            elif username_clean in ["admin", "basic", "elite", "premium"]:
                st.error("That username is reserved for backup logins.")
            elif username_exists(username_clean):
                st.error("That username already exists.")
            else:
                create_user_record(
                    username=username_clean,
                    password=password_clean,
                    role=role,
                    created_by="admin",
                    notes=notes,
                )
                st.success(f"User '{username_clean}' created successfully.")

    st.divider()

    st.subheader("Existing Users")
    users = get_sheet_data("Users")

    if users:
        st.dataframe(users, use_container_width=True)
    else:
        st.info("No sheet-based users found yet.")