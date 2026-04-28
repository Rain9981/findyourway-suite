import streamlit as st
import json
import io
import pandas as pd
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound
import gspread


def create_pdf_buffer(total, leads, active, inactive, conversion_rate, recent_clients):
    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "CRM Dashboard Summary")

    c.setFont("Helvetica", 10)
    c.drawString(100, 725, f"Total Contacts: {total}")
    c.drawString(100, 710, f"Leads: {leads}")
    c.drawString(100, 695, f"Active Clients: {active}")
    c.drawString(100, 680, f"Inactive Clients: {inactive}")
    c.drawString(100, 665, f"Lead-to-Active Conversion Rate: {conversion_rate:.1f}%")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, 640, "Recent CRM Records:")

    c.setFont("Helvetica", 9)
    y = 620
    for i, row in enumerate(recent_clients[:8]):
        line = f"{i+1}. {row.get('Name', '')} | {row.get('Status', '')} | {row.get('Email', '')}"
        c.drawString(100, y, line[:100])
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer


def get_crm_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = json.loads(st.secrets["google_sheets"]["service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])

    try:
        ws = sheet.worksheet("CRM Manager")
    except WorksheetNotFound:
        return []

    return ws.get_all_records()


def run():
    st.title("📊 CRM Dashboard")
    st.caption("View your client pipeline, lead status, activity summary, and basic CRM conversion health.")

    st.sidebar.header("💡 CRM Dashboard Guide")
    st.sidebar.markdown("""
**What this dashboard does:**
- summarizes contacts from CRM Manager
- shows lead, active, and inactive client counts
- estimates basic lead-to-active conversion rate
- helps identify whether your pipeline needs more leads, more follow-up, or stronger retention

**Best use:**
Use after adding or updating clients in CRM Manager.

**Pro Tip:** A CRM dashboard should not only show contacts. It should help you decide what needs attention next.
""")

    try:
        data = get_crm_data()

        if not data:
            st.info("No CRM records found yet. Add contacts in CRM Manager first.")
            return

        df = pd.DataFrame(data)

        if "Status" not in df.columns:
            st.warning("CRM Manager sheet must include a Status column.")
            return

        total = len(df)
        leads = len(df[df["Status"].astype(str).str.lower() == "lead"])
        active = len(df[df["Status"].astype(str).str.lower() == "active"])
        inactive = len(df[df["Status"].astype(str).str.lower() == "inactive"])

        conversion_base = leads + active
        conversion_rate = (active / conversion_base * 100) if conversion_base > 0 else 0

        st.markdown("### 📌 Pipeline Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Contacts", total)

        with col2:
            st.metric("Leads", leads)

        with col3:
            st.metric("Active Clients", active)

        with col4:
            st.metric("Inactive", inactive)

        st.markdown("### 📈 CRM Health Snapshot")

        col5, col6 = st.columns(2)

        with col5:
            st.metric("Lead-to-Active Conversion", f"{conversion_rate:.1f}%")

        with col6:
            if inactive > active:
                health_status = "Retention needs attention"
            elif leads > active:
                health_status = "Follow-up pipeline needs attention"
            elif active >= leads and active > 0:
                health_status = "Client base is active"
            else:
                health_status = "Needs more CRM data"

            st.metric("CRM Health Signal", health_status)

        st.markdown("### 🧠 Dashboard Interpretation")

        if leads > active:
            st.warning(
                "You have more leads than active clients. Focus on follow-up, conversion messaging, and moving qualified leads into action."
            )
        elif inactive > active:
            st.warning(
                "Inactive clients are higher than active clients. Review retention, reactivation emails, and client satisfaction."
            )
        elif active > 0:
            st.success(
                "Your active client base is showing strength. Continue tracking follow-up, referrals, and expansion opportunities."
            )
        else:
            st.info(
                "Your CRM needs more activity before strong conclusions can be made."
            )

        st.markdown("### 🧭 Recommended Next Moves")
        st.markdown("""
- Use **CRM Intelligence Engine** to analyze client notes and objections.
- Use **Email Marketing** to create follow-up or reactivation messages.
- Use **Lead Generation** if the lead count is low.
- Use **AI CMO Engine** if you need a broader growth strategy.
- Use **KPI Tracker** to measure conversion, follow-up, and retention.
""")

        st.markdown("### 📋 CRM Records")

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Lead", "Active", "Inactive"]
        )

        filtered_df = df.copy()

        if status_filter != "All":
            filtered_df = filtered_df[
                filtered_df["Status"].astype(str).str.lower() == status_filter.lower()
            ]

        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("### 📊 Status Breakdown")

        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)

        if st.session_state.get("user_role", "guest") == "admin":
            st.divider()
            st.markdown("### 📄 Export CRM Dashboard")

            pdf_buffer = create_pdf_buffer(
                total=total,
                leads=leads,
                active=active,
                inactive=inactive,
                conversion_rate=conversion_rate,
                recent_clients=data[:8]
            )

            st.download_button(
                "📄 Download CRM Dashboard PDF",
                pdf_buffer,
                file_name="CRM_Dashboard_Summary.pdf"
            )

    except Exception as e:
        st.warning(f"⚠️ Could not load CRM data: {e}")


if __name__ == "__main__":
    run()