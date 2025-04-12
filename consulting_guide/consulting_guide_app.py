import streamlit as st
import datetime
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

def run():
    st.title("📘 Consulting Guide")
    st.markdown("Use this guide to understand how to navigate the full consulting suite based on your tier.")

    st.sidebar.header("🧠 Consulting Guide Tips")
    st.sidebar.markdown("""
    - This guide walks through each tab in the suite.
    - Admins get a checklist to track consulting progress.
    - Export session summaries for client records.
    """)

    st.markdown("### 🔍 Tool Walkthrough Summary")

    walkthrough = {
        "Client Intake": "Start here. Collect business info, goals, and tier.",
        "Brand Positioning": "Clarify unique value, voice, and audience.",
        "Strategy Designer": "Design growth roadmap from AI suggestions.",
        "Lead Generation": "Create outreach and lead magnet plans.",
        "CRM Tabs": "Track contacts, insights, and exportable reports.",
        "Forecasting": "Predict revenue and visualize future metrics.",
        "Sentiment Analysis": "Analyze copy or client language for tone.",
        "Marketing Hub": "Generate campaigns, posts, and promotion ideas.",
        "Operations Audit": "Spot inefficiencies and get AI-powered improvements."
    }

    for tab, summary in walkthrough.items():
        st.markdown(f"**{tab}** – {summary}")

    st.divider()

    # ✅ Admin-only: Smart Checklist for consulting flow
    if st.session_state.get("user_role", "guest") == "admin":
        st.markdown("### ✅ Admin Checklist – Client Journey Progress")

        steps = [
            "Client Intake Completed",
            "Brand Positioning Finalized",
            "Strategy Designer Used",
            "Lead Gen Plan Approved",
            "CRM Records Added",
            "Forecasting Tab Used",
            "Final Report Exported"
        ]

        completed = []
        with st.form("consulting_checklist_form"):
            for step in steps:
                if st.checkbox(step, key=f"consulting_step_{step}"):
                    completed.append(step)
            submitted = st.form_submit_button("Save Progress")

        if submitted:
            st.success(f"📝 Progress Saved: {len(completed)} step(s) completed.")

        # ✅ Admin PDF Export
        if st.button("📄 Export Consulting Report to PDF"):
            buffer = io.BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, "Consulting Session Report")
            c.drawString(100, 730, f"Date: {datetime.date.today().strftime('%B %d, %Y')}")
            c.drawString(100, 710, "Completed Steps:")
            text = c.beginText(100, 695
