import streamlit as st

def run():
    st.title("🏠 Welcome to Your Consulting Suite")
    st.markdown("""
    ### 👋 Hello and welcome!

    This is your personalized AI-powered consulting dashboard for strategy, marketing, growth, and business development.

    #### 🔑 What you can do here:
    - Use AI tools to generate insights, strategy, and messaging.
    - Save all activity to Google Sheets.
    - Export consulting reports to PDF.
    - Access tabs based on your subscription tier.

    #### 📋 Quick Start Checklist:
    1. Start with **Client Intake** or **Brand Positioning**.
    2. Use GPT to generate ideas or complete forms.
    3. Save your work (auto-saves if connected).
    4. Export PDFs for your clients or team.
    """)

    st.success("✅ You're logged in and ready to begin.")
