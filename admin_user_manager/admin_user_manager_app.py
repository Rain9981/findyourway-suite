import streamlit as st
from backend.google_sheets import (
    create_user_record,
    create_users_tab_if_missing,
    get_sheet_data,
    username_exists,
    update_user_record,
    delete_user_record,
)

RESERVED_USERNAMES = ["admin", "basic", "elite", "premium"]


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
            elif username_clean in RESERVED_USERNAMES:
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
                st.rerun()

    st.divider()

    st.subheader("Existing Users")
    users = get_sheet_data("Users")

    if users:
        st.dataframe(users, use_container_width=True)
    else:
        st.info("No sheet-based users found yet.")

    st.divider()
    st.subheader("Manage Existing Users")

    users = get_sheet_data("Users")

    if not users:
        st.info("No users available to manage.")
        return

    usernames = [u["username"] for u in users if u.get("username")]
    selected_username = st.selectbox("Select a user", usernames)

    selected_user = next(
        (u for u in users if str(u.get("username", "")).strip().lower() == selected_username.strip().lower()),
        None
    )

    if not selected_user:
        st.warning("Could not load selected user.")
        return

    st.markdown(f"**Current Role:** {selected_user.get('role', '')}")
    st.markdown(f"**Current Status:** {selected_user.get('status', '')}")
    st.markdown(f"**Created At:** {selected_user.get('created_at', '')}")
    st.markdown(f"**Created By:** {selected_user.get('created_by', '')}")

    with st.form("update_user_form"):
        new_username = st.text_input("Edit Username", value=selected_user.get("username", ""))
        new_password = st.text_input(
            "New Password (leave blank to keep current password)",
            type="password"
        )
        new_role = st.selectbox(
            "Edit Role",
            ["basic", "elite", "premium", "admin"],
            index=["basic", "elite", "premium", "admin"].index(
                str(selected_user.get("role", "basic")).strip().lower()
            )
        )
        new_status = st.selectbox(
            "Edit Status",
            ["active", "inactive"],
            index=["active", "inactive"].index(
                str(selected_user.get("status", "active")).strip().lower()
            )
        )
        new_notes = st.text_area("Edit Notes", value=selected_user.get("notes", ""))

        updated = st.form_submit_button("💾 Update User")

        if updated:
            ok, msg = update_user_record(
                current_username=selected_username,
                new_username=new_username,
                new_password=new_password,
                new_role=new_role,
                new_status=new_status,
                new_notes=new_notes,
            )
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if str(selected_user.get("status", "active")).strip().lower() == "active":
            if st.button("⛔ Deactivate User"):
                ok, msg = update_user_record(
                    current_username=selected_username,
                    new_status="inactive"
                )
                if ok:
                    st.warning(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            if st.button("✅ Reactivate User"):
                ok, msg = update_user_record(
                    current_username=selected_username,
                    new_status="active"
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with col2:
        if st.button("🗑 Delete User"):
            ok, msg = delete_user_record(selected_username)
            if ok:
                st.error(msg)
                st.rerun()
            else:
                st.error(msg)