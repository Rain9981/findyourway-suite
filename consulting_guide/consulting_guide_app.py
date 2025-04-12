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
        "
