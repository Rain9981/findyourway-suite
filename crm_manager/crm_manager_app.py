import streamlit as st
import datetime
import json
import io
import pandas as pd
import gspread
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound


def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

    try:
        ws = sheet.worksheet("CRM Manager")
    except WorksheetNotFound:
        ws = sheet.add_worksheet(title="CRM Manager", rows="500", cols="20")
        ws.append_row([
            "Timestamp",
            "Name",
            "Business Name",
            "Email",
            "Phone",
            "Status",
            "Priority",
            "Source",
            "Interest Area",
            "Next Follow-Up",
            "Notes"
        ])
    return ws


def create_pdf_buffer(client_record):
    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "CRM Client Summary")

    c.setFont("Helvetica", 10)
    y = 725

    for key, value in client_record.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 18
        if y < 80:
            c.showPage()
            y = 750

    c.save()
    buffer.seek(0)
    return buffer


def run():
    st.title("🧾 CRM Manager")
    st.caption("Add, organize, and review client records for your Find Your Way consulting system.")

    st.sidebar.header("💡 CRM Manager Guide")
    st.sidebar.markdown("""
**What this tool does:**
- adds new client or lead records
- tracks status, priority, source, and follow-up
- helps organize your consulting pipeline
- feeds data into CRM Dashboard

**Best use:**
Use this before CRM Dashboard and CRM Intelligence Engine.

**Pro Tip:** A CRM is not just a contact list. It is your follow-up and relationship management system.
""")

    try:
        ws = get_worksheet()

        st.markdown("### ➕ Add New Client / Lead")

        with st.form("add_client_form_v2"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Client Name")
                business_name = st.text_input("Business Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")

            with col2:
                status = st.selectbox("Status", ["Lead", "Active", "Inactive"])
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                source = st.selectbox(
                    "Lead Source",
                    [
                        "Website",
                        "Referral",
                        "Social Media",
                        "InterNetwork",
                        "Email",
                        "Event",
                        "Manual Entry",
                        "Other"
                    ]
                )
                interest_area = st.selectbox(
                    "Interest Area",
                    [
                        "Consulting",
                        "AI Consulting Suite",
                        "Branding",
                        "Marketing",
                        "Business Development",
                        "InterNetwork",
                        "Self Enhancement",
                        "Academy",
                        "Other"
                    ]
                )

            next_follow_up = st.date_input("Next Follow-Up Date", value=datetime.date.today())
            notes = st.text_area("Client Notes", height=120)

            submitted = st.form_submit_button("✅ Add Client")

            if submitted:
                if not name.strip():
                    st.warning("Please enter a client name before saving.")
                else:
                    ws.append_row([
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        name,
                        business_name,
                        email,
                        phone,
                        status,
                        priority,
                        source,
                        interest_area,
                        str(next_follow_up),
                        notes
                    ])
                    st.success(f"✅ {name} added to CRM.")

        st.divider()

        st.markdown("### 📋 CRM Records")

        records = ws.get_all_records()

        if not records:
            st.info("No CRM records found yet.")
            return

        df = pd.DataFrame(records)

        col1, col2, col3 = st.columns(3)

        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Lead", "Active", "Inactive"])

        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High"])

        with col3:
            interest_filter = st.selectbox(
                "Filter by Interest",
                ["All"] + sorted(df["Interest Area"].dropna().astype(str).unique().tolist())
                if "Interest Area" in df.columns else ["All"]
            )

        filtered_df = df.copy()

        if status_filter != "All" and "Status" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Status"].astype(str) == status_filter]

        if priority_filter != "All" and "Priority" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Priority"].astype(str) == priority_filter]

        if interest_filter != "All" and "Interest Area" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Interest Area"].astype(str) == interest_filter]

        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("### 🧠 CRM Quick Insight")

        total = len(df)
        leads = len(df[df["Status"].astype(str).str.lower() == "lead"]) if "Status" in df.columns else 0
        active = len(df[df["Status"].astype(str).str.lower() == "active"]) if "Status" in df.columns else 0
        high_priority = len(df[df["Priority"].astype(str).str.lower() == "high"]) if "Priority" in df.columns else 0

        col4, col5, col6, col7 = st.columns(4)
        col4.metric("Total Records", total)
        col5.metric("Leads", leads)
        col6.metric("Active", active)
        col7.metric("High Priority", high_priority)

        if high_priority > 0:
            st.warning("You have high-priority contacts that may need follow-up.")
        elif leads > active:
            st.info("Your lead pool is larger than your active client base. Focus on follow-up and conversion.")
        else:
            st.success("CRM is organized. Continue tracking follow-ups and client movement.")

        if st.session_state.get("user_role", "guest") == "admin":
            st.divider()
            st.markdown("### 📄 Export Client Summary")

            names = filtered_df["Name"].dropna().astype(str).tolist() if "Name" in filtered_df.columns else []

            if names:
                selected_name = st.selectbox("Select a client to export:", names)
                selected_row = filtered_df[filtered_df["Name"].astype(str) == selected_name].iloc[0].to_dict()

                pdf_buffer = create_pdf_buffer(selected_row)

                st.download_button(
                    "📄 Download Client Summary PDF",
                    pdf_buffer,
                    file_name=f"{selected_name}_CRM_Summary.pdf"
                )

    except Exception as e:
        st.warning(f"⚠️ CRM Manager could not load: {e}")


if __name__ == "__main__":
    run()