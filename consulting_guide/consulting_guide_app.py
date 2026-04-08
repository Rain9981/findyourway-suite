import streamlit as st
import datetime
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def run():
    st.title("📘 Consulting Guide")
    st.markdown(
        """
        Use this guide to move through the Find Your Way Consulting Suite in a clean and strategic order.
        Each tool below explains what it does, why it matters, when to use it, what it pairs with next,
        and which FYW program, module, or service it naturally connects to.
        """
    )

    st.sidebar.header("🧠 Consulting Guide Tips")
    st.sidebar.markdown(
        """
        - Follow the numbered flow if you want the smoothest consulting journey.
        - Use the "Where Should I Start?" section if you already know what kind of help you need.
        - Check the FYW Recommendation line to connect each tool to the right program or service.
        """
    )

    st.markdown("## 1️⃣ Suggested Consulting Flow")
    flow_steps = [
        "Homepage",
        "Subscription Plans",
        "Consulting Guide",
        "Client Intake",
        "Brand Positioning",
        "Business Development",
        "Strategy Designer",
        "Business Model Canvas",
        "Business Genius Engine",
        "Lead Generation",
        "Marketing Hub",
        "Marketing Planner",
        "Email Marketing",
        "Sentiment Analysis",
        "Mastermind Analyzer",
        "Operations Audit",
        "Oops Audit",
        "Self Enhancement",
        "Growth",
        "KPI Tracker",
        "Forecasting",
        "Credit Repair",
        "Canvas",
        "CRM Manager / CRM / CRM Dashboard"
    ]

    for i, step in enumerate(flow_steps, start=1):
        st.markdown(f"**{i}. {step}**")

    st.divider()

    st.markdown("## 2️⃣ Where Should I Start?")
    start_points = {
        "I am brand new and need direction": [
            "Homepage",
            "Subscription Plans",
            "Consulting Guide",
            "Client Intake"
        ],
        "I need help clarifying my brand": [
            "Brand Positioning",
            "Strategy Designer",
            "Business Model Canvas"
        ],
        "I need more leads and visibility": [
            "Lead Generation",
            "Marketing Hub",
            "Marketing Planner",
            "Email Marketing"
        ],
        "I need stronger strategy and decision-making": [
            "Business Development",
            "Strategy Designer",
            "Business Genius Engine",
            "Mastermind Analyzer"
        ],
        "I need to fix inefficiencies or weak systems": [
            "Operations Audit",
            "Oops Audit",
            "KPI Tracker",
            "Forecasting"
        ],
        "I want growth and scaling support": [
            "Growth",
            "Forecasting",
            "KPI Tracker",
            "Business Development"
        ],
        "I want mindset and leadership support too": [
            "Self Enhancement",
            "Strategy Designer",
            "Growth"
        ]
    }

    for need, tools in start_points.items():
        st.markdown(f"**{need}**")
        st.markdown(" → " + " → ".join(tools))

    st.divider()

    st.markdown("## 3️⃣ Tool Directory")

    tool_guide = [
        {
            "name": "🏠 Homepage",
            "purpose": "Your entry point into the suite with a high-level overview of the tools and how they connect.",
            "benefit": "Helps you quickly understand the consulting journey and where to begin.",
            "best_time": "Use first when entering the suite.",
            "pairs_with": "Subscription Plans, Consulting Guide, Client Intake",
            "recommendation": "Best paired with the FYW onboarding path and your initial consulting starting point."
        },
        {
            "name": "💳 Subscription Plans",
            "purpose": "Shows the available access tiers and feature levels.",
            "benefit": "Helps you choose the right support level based on your business needs.",
            "best_time": "Use early if you need to understand access options before moving deeper.",
            "pairs_with": "Consulting Guide, Client Intake",
            "recommendation": "Pairs with your FYW service access path and tier selection process."
        },
        {
            "name": "📘 Consulting Guide",
            "purpose": "Explains how to use the suite in the right order and what each tool is for.",
            "benefit": "Saves time and removes confusion by guiding clients clearly.",
            "best_time": "Use before or during your suite journey whenever you need clarity.",
            "pairs_with": "Homepage, Client Intake, any next tool",
            "recommendation": "Acts as the bridge between the suite and the broader FYW consulting ecosystem."
        },
        {
            "name": "🧠 Future Self Deep State",
            "purpose": "Analyzes identity, fear patterns, and future trajectory based on your current situation.",
            "benefit": "Helps you see what is really shaping your decisions and where your life is heading if nothing changes.",
            "best_time": "Use when you feel stuck, unclear, or know you are not fully stepping into your potential.",
            "pairs_with": "Self Enhancement, Strategy Designer, Business Genius Engine",
            "recommendation": "Best matched with FYW Self-Enhancement programs and Legacy Architecture for deeper identity and structural       	    transformation."
        }
        {
            "name": "📝 Client Intake",
            "purpose": "Captures business details, goals, and challenges to create a tailored consulting path.",
            "benefit": "Ensures the strategy is based on the client's real needs instead of assumptions.",
            "best_time": "Use early before deeper strategy work begins.",
            "pairs_with": "Brand Positioning, Business Development, Strategy Designer",
            "recommendation": "Pairs with FYW intake, consulting diagnosis, and service matching."
        },
        {
            "name": "🎯 Brand Positioning",
            "purpose": "Defines your unique value, voice, audience, and market position.",
            "benefit": "Helps you stand out and attract the right people more effectively.",
            "best_time": "Use near the beginning before major marketing or growth work.",
            "pairs_with": "Strategy Designer, Marketing Hub, Business Development",
            "recommendation": "Best matched with the FYW Branding module and brand strategy services."
        },
        {
            "name": "📈 Business Development",
            "purpose": "Identifies growth opportunities, partnerships, and ways to expand strategically.",
            "benefit": "Helps the business move beyond survival and toward stronger scale opportunities.",
            "best_time": "Use once the brand foundation is becoming clear.",
            "pairs_with": "Strategy Designer, Business Model Canvas, Growth",
            "recommendation": "Best matched with FYW Business Development consulting and expansion strategy support."
        },
        {
            "name": "🗂 Business Model Canvas",
            "purpose": "Maps your business model across offers, value, audience, channels, and revenue structure.",
            "benefit": "Gives a full-picture view of how the business actually works.",
            "best_time": "Use when refining business structure or validating a model.",
            "pairs_with": "Business Development, Strategy Designer, Business Genius Engine",
            "recommendation": "Pairs with FYW business structure, offer clarity, and model refinement work."
        },
        {
            "name": "🛠 Strategy Designer",
            "purpose": "Builds a practical roadmap using AI-supported strategic thinking.",
            "benefit": "Turns broad ideas into a step-by-step plan.",
            "best_time": "Use after intake, brand clarification, or business review.",
            "pairs_with": "Brand Positioning, Business Development, Growth",
            "recommendation": "Best matched with FYW strategy planning and high-level consulting support."
        },
        {
            "name": "🤖 Business Genius Engine",
            "purpose": "Generates new ideas, advanced insights, and future-focused strategies.",
            "benefit": "Unlocks solutions and options clients may not have considered on their own.",
            "best_time": "Use when deeper creative or strategic thinking is needed.",
            "pairs_with": "Business Development, Strategy Designer, Mastermind Analyzer",
            "recommendation": "Pairs with advanced FYW strategy, innovation, and CMO-style advisory support."
        },
        {
            "name": "📩 Lead Generation",
            "purpose": "Helps create outreach plans, lead magnets, and prospect strategies.",
            "benefit": "Builds a stronger path to attracting qualified leads consistently.",
            "best_time": "Use after your offer and positioning are clear.",
            "pairs_with": "Marketing Hub, Email Marketing, Marketing Planner",
            "recommendation": "Best matched with FYW Lead Generation and growth-focused marketing services."
        },
        {
            "name": "📢 Marketing Hub",
            "purpose": "Develops campaign concepts, promotional ideas, and content direction.",
            "benefit": "Improves visibility and strengthens brand communication.",
            "best_time": "Use when you are ready to promote more intentionally.",
            "pairs_with": "Lead Generation, Marketing Planner, Sentiment Analysis",
            "recommendation": "Pairs with FYW Marketing services, campaign support, and promotional strategy."
        },
        {
            "name": "🗓 Marketing Planner",
            "purpose": "Turns marketing ideas into a more structured and scheduled execution path.",
            "benefit": "Keeps campaigns organized and aligned with goals.",
            "best_time": "Use after campaign ideas are developed.",
            "pairs_with": "Marketing Hub, Email Marketing, KPI Tracker",
            "recommendation": "Best matched with FYW campaign execution and planning support."
        },
        {
            "name": "✉️ Email Marketing",
            "purpose": "Builds email sequences and campaigns for follow-up, nurturing, and sales support.",
            "benefit": "Helps convert leads and maintain stronger communication.",
            "best_time": "Use after lead strategy and campaign direction are in place.",
            "pairs_with": "Lead Generation, Marketing Planner, Sentiment Analysis",
            "recommendation": "Pairs with FYW Email Campaign services and nurture-based marketing support."
        },
        {
            "name": "💬 Sentiment Analysis",
            "purpose": "Reviews messaging tone, persuasion, and emotional impact.",
            "benefit": "Helps make your words land more effectively before publishing.",
            "best_time": "Use before finalizing campaigns, copy, or communication pieces.",
            "pairs_with": "Marketing Hub, Email Marketing, Mastermind Analyzer",
            "recommendation": "Best matched with FYW messaging refinement, brand voice, and communication improvement work."
        },
        {
            "name": "🧠 Mastermind Analyzer",
            "purpose": "Compares ideas, strategies, or offers using AI-driven pros and cons.",
            "benefit": "Helps you make stronger decisions with more confidence.",
            "best_time": "Use when deciding between multiple paths or offers.",
            "pairs_with": "Business Genius Engine, Strategy Designer, Sentiment Analysis",
            "recommendation": "Pairs with FYW advanced planning, decision support, and strategic advisory services."
        },
        {
            "name": "🔍 Operations Audit",
            "purpose": "Looks for workflow issues, inefficiencies, and system weaknesses.",
            "benefit": "Helps improve performance, save time, and reduce unnecessary friction.",
            "best_time": "Use when the business feels disorganized, slow, or inconsistent.",
            "pairs_with": "Oops Audit, KPI Tracker, Forecasting",
            "recommendation": "Best matched with FYW systems, operations, and infrastructure consulting."
        },
        {
            "name": "⚠️ Oops Audit",
            "purpose": "Helps surface mistakes, blind spots, and overlooked issues in strategy or execution.",
            "benefit": "Makes it easier to fix problems before they grow.",
            "best_time": "Use after reviewing campaigns, operations, or growth plans.",
            "pairs_with": "Operations Audit, Growth, KPI Tracker",
            "recommendation": "Pairs with FYW diagnostic consulting and optimization services."
        },
        {
            "name": "💪 Self Enhancement",
            "purpose": "Supports mindset, leadership growth, clarity, and personal development.",
            "benefit": "Improves the person behind the business, not just the business itself.",
            "best_time": "Use when confidence, focus, decision-making, or discipline need support.",
            "pairs_with": "Growth, Strategy Designer, Business Genius Engine",
            "recommendation": "Best matched with FYW Self-Enhancement modules and transformation-based programs."
        },
        {
            "name": "📊 Growth",
            "purpose": "Explores scaling opportunities and bigger-picture business expansion ideas.",
            "benefit": "Helps move from maintenance mode into intentional growth mode.",
            "best_time": "Use when you are ready to expand, optimize, or reach more people.",
            "pairs_with": "Business Development, KPI Tracker, Forecasting",
            "recommendation": "Pairs with FYW growth strategy, scaling services, and expansion support."
        },
        {
            "name": "📌 KPI Tracker",
            "purpose": "Tracks performance metrics against goals and expectations.",
            "benefit": "Makes progress measurable and easier to manage.",
            "best_time": "Use after plans and campaigns are in motion.",
            "pairs_with": "Growth, Forecasting, Operations Audit",
            "recommendation": "Best matched with FYW performance review, optimization, and accountability support."
        },
        {
            "name": "📉 Forecasting",
            "purpose": "Projects future performance, revenue direction, and potential trends.",
            "benefit": "Supports better planning through clearer expectations.",
            "best_time": "Use when making growth decisions or planning the next move.",
            "pairs_with": "Growth, KPI Tracker, Business Development",
            "recommendation": "Pairs with FYW planning, scale forecasting, and long-range strategy support."
        },
        {
            "name": "💳 Credit Repair",
            "purpose": "Supports personal or business credit improvement where needed.",
            "benefit": "Can improve financial readiness and funding options.",
            "best_time": "Use when credit is a barrier to business growth or opportunity.",
            "pairs_with": "Business Development, Growth",
            "recommendation": "Best matched with FYW credit support access and financial readiness pathways."
        },
        {
            "name": "🎨 Canvas",
            "purpose": "Helps visualize ideas, concepts, or structures in a more creative format.",
            "benefit": "Makes it easier to organize vision and communicate direction.",
            "best_time": "Use during ideation, planning, or when structure needs visual clarity.",
            "pairs_with": "Business Model Canvas, Strategy Designer, Business Genius Engine",
            "recommendation": "Pairs with FYW vision-mapping, concept planning, and creative strategy support."
        },
        {
            "name": "📇 CRM Manager",
            "purpose": "Stores and manages client and contact information.",
            "benefit": "Keeps important relationship data organized and accessible.",
            "best_time": "Use during active client management or service delivery.",
            "pairs_with": "CRM, CRM Dashboard",
            "recommendation": "Best matched with FYW backend consulting, systems management, and admin workflow support."
        },
        {
            "name": "🧾 CRM",
            "purpose": "Supports relationship tracking, notes, and deeper client management workflows.",
            "benefit": "Helps maintain stronger follow-up and client organization.",
            "best_time": "Use after intake and throughout the client relationship.",
            "pairs_with": "CRM Manager, CRM Dashboard",
            "recommendation": "Pairs with FYW CRM setup, backend workflow, and systems support."
        },
        {
            "name": "📊 CRM Dashboard",
            "purpose": "Provides a visual look at client activity, status, and relationship health.",
            "benefit": "Makes it easier to spot opportunities, follow-up needs, and risks.",
            "best_time": "Use when monitoring multiple clients or ongoing consulting relationships.",
            "pairs_with": "CRM Manager, CRM",
            "recommendation": "Best matched with FYW backend management, consulting oversight, and relationship intelligence."
        }
    ]

    for tool in tool_guide:
        st.markdown(f"### {tool['name']}")
        st.markdown(f"**Purpose:** {tool['purpose']}")
        st.markdown(f"**Benefit:** {tool['benefit']}")
        st.markdown(f"**Best Time to Use:** {tool['best_time']}")
        st.markdown(f"**Pairs Well With:** {tool['pairs_with']}")
        st.markdown(f"**FYW Recommendation:** {tool['recommendation']}")
        st.markdown("---")

    st.markdown("## 4️⃣ Quick Tier Reminder")
    st.markdown(
        """
        - **Basic** gives a focused starting point for guidance, positioning, and planning.
        - **Elite** expands into stronger growth, marketing, and strategy support.
        - **Premium** opens more advanced execution and communication tools.
        - **Admin** includes the full suite plus backend management tools.
        """
    )

    st.divider()

    if st.session_state.get("user_role", "guest") == "admin":
        st.markdown("## 5️⃣ Admin Checklist – Client Journey Progress")

        steps = [
            "Homepage Reviewed",
            "Subscription Tier Confirmed",
            "Client Intake Completed",
            "Brand Positioning Completed",
            "Strategy Designer Used",
            "Business Development Reviewed",
            "Lead Generation Plan Built",
            "Marketing Hub Used",
            "Marketing Planner Reviewed",
            "Email Marketing Drafted",
            "Sentiment Analysis Checked",
            "Operations Audit Reviewed",
            "Growth Strategy Reviewed",
            "KPI Tracker Used",
            "Forecasting Completed",
            "CRM Updated",
            "Final Recommendations Shared"
        ]

        completed = []

        with st.form("consulting_checklist_form"):
            for step in steps:
                if st.checkbox(step, key=f"consulting_step_{step}"):
                    completed.append(step)
            submitted = st.form_submit_button("Save Progress")

        if submitted:
            st.success(f"📝 Progress Saved: {len(completed)} step(s) completed.")

        if st.button("📄 Export Consulting Report to PDF"):
            buffer = io.BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=letter)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(72, 750, "Find Your Way Consulting Session Report")

            c.setFont("Helvetica", 11)
            c.drawString(72, 730, f"Date: {datetime.date.today().strftime('%B %d, %Y')}")
            c.drawString(72, 710, f"Admin User: {st.session_state.get('user_role', 'admin').capitalize()}")

            text = c.beginText(72, 685)
            text.setFont("Helvetica", 11)
            text.textLine("Completed Steps:")
            text.textLine("")

            if completed:
                for step in completed:
                    text.textLine(f"- {step}")
            else:
                text.textLine("No steps were selected.")

            text.textLine("")
            text.textLine("Use this report as a lightweight summary of the consulting path reviewed.")
            c.drawText(text)

            c.save()
            buffer.seek(0)

            st.download_button(
                "Download PDF",
                buffer,
                file_name="consulting_session_report.pdf",
                mime="application/pdf"
            )