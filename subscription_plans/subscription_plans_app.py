import streamlit as st
import io
import datetime
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def run():
    st.title("💳 Subscription Plans")
    st.markdown(
        """
        The Find Your Way AI Consulting Suite is connected to the **FYW InterNetwork membership system**.
        Inside the app, access is organized as **Basic, Elite, and Premium**.
        Externally, these tiers connect to the InterNetwork membership path that unlocks access.
        """
    )

    st.sidebar.header("📘 Plan Guide")
    st.sidebar.markdown(
        """
        - Compare each monthly access level below.
        - See which tabs are included with each tier.
        - Upgrade through the official FYW InterNetwork membership page.
        """
    )

    st.markdown("## 🔗 How Access Connects to FYW InterNetwork")
    st.markdown(
        """
        The consulting suite strengthens the **FYW InterNetwork** by connecting membership enrollment directly
        to app access.

        **Inside the App → Membership Connection**
        - **Basic** access = **Affiliate Membership – $19.99/month**
        - **Elite** access = **Business Partner Membership – $49.99/month**
        - **Premium** access = **Executive Circle Membership – $99.99/month**

        This allows members to join through the InterNetwork while receiving the matching level of consulting suite access.
        """
    )

    st.divider()

    st.markdown("## 🧾 Membership Levels")

    st.markdown("### Basic Access — $19.99/month")
    st.markdown(
        """
        **InterNetwork Connection:** **Affiliate Membership**

        **Best for:** getting started, building clarity, and using foundational consulting tools.

        **Included Tabs:**
        - Homepage
        - Subscription Plans
        - Consulting Guide
        - Brand Positioning
        - Strategy Designer
        - Network Builder
        - Credit Repair
        - Future Self Deep State
        """
    )

    st.markdown("### Elite Access — $49.99/month")
    st.markdown(
        """
        **InterNetwork Connection:** **Business Partner Membership**

        **Best for:** stronger strategy, business development, marketing direction, and growth planning.

        **Included Tabs:**
        - Homepage
        - Subscription Plans
        - Consulting Guide
        - Brand Positioning
        - Business Development
        - Strategy Designer
        - Lead Generation
        - Network Builder
        - Marketing Hub
        - AI CMO Engine
        - Strategic Simulator
        - Operations Audit
        - Growth
        - KPI Tracker
        - Forecasting
        - Credit Repair
        - Find Where You Win
        - Future Self Deep State
        """
    )

    st.markdown("### Premium Access — $99.99/month")
    st.markdown(
        """
        **InterNetwork Connection:** **Executive Circle Membership**

        **Best for:** deeper execution, advanced communication tools, expanded planning, and premium-level support.

        **Included Tabs:**
        - Homepage
        - Subscription Plans
        - Consulting Guide
        - Brand Positioning
        - Business Development
        - Strategy Designer
        - Lead Generation
        - Network Builder
        - Marketing Hub
        - Marketing Planner
        - Email Marketing
        - AI CMO Engine
        - Strategic Simulator
        - Sentiment Analysis
        - Operations Audit
        - Oops Audit
        - Growth
        - KPI Tracker
        - Forecasting
        - Canvas
        - Credit Repair
        - Find Where You Win
        - Future Self Deep State
        """
    )

    st.markdown("### Admin Access")
    st.markdown(
        """
        **Internal Level:** Full Suite Control

        **Best for:** backend management, consulting delivery, CRM oversight, and full system administration.

        **Included Tabs:**
        - Homepage
        - Subscription Plans
        - Consulting Guide
        - Client Intake
        - Brand Positioning
        - Business Development
        - Strategy Designer
        - Business Model Canvas
        - Business Genius Engine
        - Lead Generation
        - Network Builder
        - Marketing Hub
        - Marketing Planner
        - Email Marketing
        - AI CMO Engine
        - Strategic Simulator
        - Sentiment Analysis
        - Mastermind Analyzer
        - Operations Audit
        - Oops Audit
        - Self Enhancement
        - Growth
        - KPI Tracker
        - Forecasting
        - Credit Repair
        - Find Where You Win
        - Future Self Deep State
        - Canvas
        - CRM Manager
        - CRM
        - CRM Dashboard
        - Admin User Manager
        """
    )

    st.divider()

    st.markdown("## 📊 Quick Access Comparison")

    comparison_rows = [
        ["Homepage", "✅", "✅", "✅", "✅"],
        ["Subscription Plans", "✅", "✅", "✅", "✅"],
        ["Consulting Guide", "✅", "✅", "✅", "✅"],
        ["Future Self Deep State", "✅", "✅", "✅", "✅"],
        ["Client Intake", "🔒", "🔒", "🔒", "✅"],
        ["Brand Positioning", "✅", "✅", "✅", "✅"],
        ["Business Development", "🔒", "✅", "✅", "✅"],
        ["Strategy Designer", "✅", "✅", "✅", "✅"],
        ["Business Model Canvas", "🔒", "🔒", "🔒", "✅"],
        ["Business Genius Engine", "🔒", "🔒", "🔒", "✅"],
        ["Lead Generation", "🔒", "✅", "✅", "✅"],
        ["Network Builder", "✅", "✅", "✅", "✅"],
        ["Marketing Hub", "🔒", "✅", "✅", "✅"],
        ["Marketing Planner", "🔒", "🔒", "✅", "✅"],
        ["Email Marketing", "🔒", "🔒", "✅", "✅"],
        ["AI CMO Engine", "🔒", "✅", "✅", "✅"],
        ["Strategic Simulator", "🔒", "✅", "✅", "✅"],
        ["Sentiment Analysis", "🔒", "🔒", "✅", "✅"],
        ["Mastermind Analyzer", "🔒", "🔒", "🔒", "✅"],
        ["Operations Audit", "🔒", "✅", "✅", "✅"],
        ["Oops Audit", "🔒", "🔒", "✅", "✅"],
        ["Self Enhancement", "🔒", "🔒", "🔒", "✅"],
        ["Growth", "🔒", "✅", "✅", "✅"],
        ["KPI Tracker", "🔒", "✅", "✅", "✅"],
        ["Forecasting", "🔒", "✅", "✅", "✅"],
        ["Credit Repair", "✅", "✅", "✅", "✅"],
        ["Find Where You Win™", "❌", "✅", "✅", "✅"],
        ["Canvas", "🔒", "🔒", "✅", "✅"],
        ["CRM Manager", "🔒", "🔒", "🔒", "✅"],
        ["CRM", "🔒", "🔒", "🔒", "✅"],
        ["CRM Dashboard", "🔒", "🔒", "🔒", "✅"],
        ["Admin User Manager", "🔒", "🔒", "🔒", "✅"],
    ]

    st.table(
        {
            "Tool / Access": [row[0] for row in comparison_rows],
            "Basic ($19.99/mo)": [row[1] for row in comparison_rows],
            "Elite ($49.99/mo)": [row[2] for row in comparison_rows],
            "Premium ($99.99/mo)": [row[3] for row in comparison_rows],
            "Admin": [row[4] for row in comparison_rows],
        }
    )

    st.divider()

    st.markdown("## 🚀 Upgrade Through FYW InterNetwork")
    st.markdown(
        """
        Your consulting suite access is connected to the FYW InterNetwork membership pathway.

        **Upgrade your membership here:**  
        [FYW InterNetwork Membership](https://findyourwaynmc.com/internetwork#internetwork-membership)
        """
    )

    st.info(
        "Basic access is tied to the Affiliate Membership at $19.99/month, Elite access is tied to the Business Partner Membership at $49.99/month, and Premium access is tied to the Executive Circle Membership at $99.99/month."
    )

    if st.session_state.get("user_role", "guest") == "admin":
        st.divider()
        st.markdown("## 📄 Admin Export")

        if st.button("Export Plans to PDF"):
            buffer = io.BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=letter)

            y = 750
            c.setFont("Helvetica-Bold", 16)
            c.drawString(72, y, "Find Your Way - Subscription Plans Overview")

            y -= 24
            c.setFont("Helvetica", 10)
            c.drawString(72, y, f"Generated: {datetime.date.today().strftime('%B %d, %Y')}")

            y -= 30
            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, y, "InterNetwork Membership Connection")

            y -= 18
            c.setFont("Helvetica", 10)
            lines = [
                "Basic = Affiliate Membership ($19.99/month)",
                "Elite = Business Partner Membership ($49.99/month)",
                "Premium = Executive Circle Membership ($99.99/month)",
                "Admin = Internal Full Access Level",
            ]

            for line in lines:
                c.drawString(72, y, f"- {line}")
                y -= 16

            y -= 14
            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, y, "Tier Summary")

            y -= 18
            c.setFont("Helvetica", 10)
            summary_lines = [
                "Basic: foundational planning and entry-level consulting tools.",
                "Elite: adds strategy, marketing direction, and growth tools.",
                "Premium: adds expanded execution and communication tools.",
                "Admin: includes the full suite, CRM tools, intake, and user management.",
            ]

            for line in summary_lines:
                c.drawString(72, y, f"- {line}")
                y -= 16

            y -= 14
            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, y, "Upgrade Link")

            y -= 18
            c.setFont("Helvetica", 10)
            c.drawString(72, y, "findyourwaynmc.com/internetwork#internetwork-membership")

            c.save()
            buffer.seek(0)

            st.download_button(
                "Download PDF",
                buffer,
                file_name="subscription_plans_overview.pdf",
                mime="application/pdf"
            )