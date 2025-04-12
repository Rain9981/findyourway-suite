import streamlit as st
import io
import datetime
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

def run():
    st.title("💳 Subscription Plans")
    st.markdown("Choose the right plan for your business goals.")

    st.sidebar.header("📘 Plan Guide")
    st.sidebar.markdown("""
    - Compare plan features and benefits.
    - Upgrade your access by contacting admin.
    - Admins can export this info for clients.
    """)

    # 📊 Plan Comparison Table
    st.markdown("### 🧾 Plan Overview")
    plan_data = {
        "Feature": [
            "Access to Forecasting Tools",
            "Access to CRM Tabs",
            "AI Strategy Designer",
            "Google Sheets Sync",
            "PDF Export",
            "Client Insights (AI)",
            "Admin Dashboard Access"
        ],
        "Basic ($19.99)": ["✅", "🔒", "🔒", "✅", "🔒", "🔒", "🔒"],
        "Elite ($49.99)": ["✅", "✅", "✅", "✅", "✅", "✅", "🔒"],
        "Premium ($99.99)": ["✅", "✅", "✅", "✅", "✅", "✅", "🔒"],
        "Admin": ["✅", "✅", "✅", "✅", "✅", "✅", "✅"]
    }

    st.table(plan_data)

    st.markdown("""
    🔒 **Upgrade your access** by contacting support at  
    📧 `support@findyourwaynmc.com` or through the CRM intake tab.
    """)

    # ✅ Admin PDF Export
    if st.session_state.get("user_role", "guest") == "admin":
        if st.button("📄 Export Plans to PDF"):
            buffer = io.BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, "Find Your Way - Subscription Plans Overview")
            c.drawString(100, 730, "Basic: Limited Access | Elite: Full Tools | Premium: Advanced AI | Admin: Full Control")
            c.drawString(100, 700, "Key Features Per Plan:")
            c.drawString(100, 680, "✓ Forecasting, CRM, Strategy Tools, Sheets Sync, PDF Export, GPT Insights, Admin Access")
            c.save()
            buffer.seek(0)
            st.download_button("Download PDF", buffer, file_name="subscription_plans.pdf")
