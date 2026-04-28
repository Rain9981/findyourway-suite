import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_intake_prompt(
    client_name,
    business_name,
    industry,
    stage,
    goal,
    challenge,
    current_systems,
    support_needed,
    readiness,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in intake diagnosis and system routing mode.

Analyze this client and return:

1. Client Snapshot
2. Business Stage Interpretation
3. Core Problem
4. Primary Opportunity
5. Recommended Pathway (choose ONE):
   - Identity & Clarity Path
   - Business Foundation Path
   - Strategy & Growth Path
   - Marketing & Lead Path
   - CRM & Conversion Path
6. Recommended Tabs (list specific tabs)
7. First Tab to Start With
8. Service Recommendation (if any)
9. Risk / Blind Spot
10. Next 3 Actions
11. Final Insight

Client Name: {client_name}
Business Name: {business_name}
Industry: {industry}
Stage: {stage}
Goal: {goal}
Challenge: {challenge}
Current Systems: {current_systems}
Support Needed: {support_needed}
Readiness: {readiness}
Notes: {optional_notes if optional_notes.strip() else "None provided"}

Available FYW Tabs:
- Homepage
- Subscription Plans
- Consulting Guide
- Client Intake
- Find Where You Win
- Self Enhancement
- Future Self Deep State
- Canvas
- Business Model Canvas
- Brand Positioning
- Business Genius Engine
- AI CMO Engine
- Strategy Designer
- Strategic Simulator
- Business Development
- Growth
- Marketing Hub
- Marketing Planner
- Email Marketing
- Lead Generation
- Network Builder
- KPI Tracker
- Forecasting
- CRM Manager
- CRM Dashboard
- CRM Intelligence
- Operations Audit
- Oops Audit
- Sentiment Analysis
- Mastermind Analyzer
- Credit Repair
"""


def create_pdf_buffer(title, output):
    buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 40, title)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")

    text = pdf.beginText(50, height - 90)
    text.setFont("Helvetica", 10)

    y = height - 90
    for line in output.split("\n"):
        if y < 50:
            pdf.drawText(text)
            pdf.showPage()
            text = pdf.beginText(50, height - 50)
            text.setFont("Helvetica", 10)
            y = height - 50
        text.textLine(line[:110])
        y -= 12

    pdf.drawText(text)
    pdf.save()
    buffer.seek(0)
    return buffer


def get_recommended_tabs(output):
    output_lower = output.lower()

    if "identity & clarity path" in output_lower or "identity" in output_lower or "clarity" in output_lower:
        return [
            "Find Where You Win",
            "Self Enhancement",
            "Future Self Deep State"
        ]

    if "business foundation path" in output_lower or "foundation" in output_lower or "business model" in output_lower:
        return [
            "Canvas",
            "Business Model Canvas",
            "Brand Positioning",
            "Business Genius Engine"
        ]

    if "strategy & growth path" in output_lower or "strategy" in output_lower or "growth" in output_lower:
        return [
            "AI CMO Engine",
            "Strategy Designer",
            "Strategic Simulator",
            "Growth"
        ]

    if "marketing & lead path" in output_lower or "marketing" in output_lower or "lead" in output_lower:
        return [
            "Marketing Hub",
            "Marketing Planner",
            "Email Marketing",
            "Lead Generation",
            "Network Builder"
        ]

    if "crm & conversion path" in output_lower or "crm" in output_lower or "conversion" in output_lower:
        return [
            "CRM Manager",
            "CRM Dashboard",
            "CRM Intelligence"
        ]

    return [
        "Consulting Guide",
        "AI CMO Engine",
        "Growth"
    ]


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("📝 Client Intake")
    st.caption("Diagnose the client and route them into the correct pathway inside the FYW system.")

    st.sidebar.header("💡 Client Intake Guide")
    st.sidebar.markdown("""
**What this tool does:**
- collects client/business context
- diagnoses the client’s current stage
- assigns the best pathway
- recommends exact FYW tabs to use next
- creates a clear starting point for consulting

**Best use:**
Use this before running other tools when a client is new, unclear, or needs direction.

**Pro Tip:** Intake is not just data collection. It is the first diagnosis of where the client should go next.
""")

    defaults = {
        "client_name": "",
        "business_name": "",
        "industry": "",
        "stage": "Growing",
        "goal": "",
        "challenge": "",
        "systems": "",
        "support": "",
        "readiness": "Exploring options",
        "notes": "",
        "intake_result": "",
        "recommended_next_tabs": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["client_name"] = "James Bailey"
        st.session_state["business_name"] = "Better N Clean"
        st.session_state["industry"] = "Residential and Commercial Cleaning"
        st.session_state["stage"] = "Growing"
        st.session_state["goal"] = "Get more consistent residential and commercial clients."
        st.session_state["challenge"] = "The business relies too much on word of mouth and does not have a clear marketing or follow-up system."
        st.session_state["systems"] = "Some Facebook posting, word of mouth, flyers, and occasional direct outreach."
        st.session_state["support"] = "Marketing strategy, lead generation, CRM follow-up, brand positioning, and growth planning."
        st.session_state["readiness"] = "Ready for structured support"
        st.session_state["notes"] = "Client wants a professional system that can bring in consistent residential and commercial leads."

    st.markdown("### 📥 Client Intake Input")

    col1, col2 = st.columns(2)

    with col1:
        client_name = st.text_input("Client Name", key="client_name")
        business_name = st.text_input("Business Name", key="business_name")
        industry = st.text_input("Industry / Niche", key="industry")

    with col2:
        stage = st.selectbox(
            "Business Stage",
            ["Idea Stage", "Startup", "Growing", "Established", "Scaling"],
            key="stage"
        )

        readiness = st.selectbox(
            "Readiness Level",
            [
                "Just exploring",
                "Exploring options",
                "Needs low-cost starting point",
                "Ready for structured support",
                "Ready to invest soon",
                "High-ticket ready"
            ],
            key="readiness"
        )

    goal = st.text_area(
        "Primary Goal",
        key="goal",
        height=100,
        placeholder="What does the client want to accomplish?"
    )

    challenge = st.text_area(
        "Main Challenge",
        key="challenge",
        height=100,
        placeholder="What is blocking progress right now?"
    )

    current_systems = st.text_area(
        "Current Marketing / Systems",
        key="systems",
        height=100,
        placeholder="What are they currently using for marketing, CRM, operations, or follow-up?"
    )

    support_needed = st.text_area(
        "Support Needed",
        key="support",
        height=100,
        placeholder="What kind of help do they need?"
    )

    optional_notes = st.text_area(
        "Additional Notes",
        key="notes",
        height=100,
        placeholder="Add any important context from the conversation."
    )

    if st.button("🚀 Diagnose & Route Client"):
        required = [
            client_name.strip(),
            business_name.strip(),
            industry.strip(),
            goal.strip(),
            challenge.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main intake fields before generating.")
        else:
            try:
                with st.spinner("Diagnosing client and building recommended path..."):
                    prompt = build_intake_prompt(
                        client_name=client_name,
                        business_name=business_name,
                        industry=industry,
                        stage=stage,
                        goal=goal,
                        challenge=challenge,
                        current_systems=current_systems,
                        support_needed=support_needed,
                        readiness=readiness,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in client intake routing mode: strategic, practical, "
                                    "clear, and focused on diagnosing the correct FYW pathway and next tool sequence."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.75,
                    )

                    output = response.choices[0].message.content
                    st.session_state["intake_result"] = output
                    st.session_state["recommended_next_tabs"] = get_recommended_tabs(output)

                    try:
                        save_data("Client_Intake", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Client_Name": client_name,
                            "Business_Name": business_name,
                            "Industry": industry,
                            "Business_Stage": stage,
                            "Readiness": readiness,
                            "Primary_Goal": goal,
                            "Main_Challenge": challenge,
                            "Current_Systems": current_systems,
                            "Support_Needed": support_needed,
                            "Optional_Notes": optional_notes,
                            "Recommended_Tabs": ", ".join(st.session_state["recommended_next_tabs"]),
                            "Intake_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Client routed successfully.")
                st.subheader("📝 Client Intake Strategy")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("intake_result"):
        st.divider()

        st.markdown("### 🧭 Recommended Next Tabs")

        for tab in st.session_state.get("recommended_next_tabs", []):
            if st.button(f"➡️ Go to {tab}", key=f"go_to_{tab}"):
                st.session_state["suggested_tab"] = tab
                st.info(f"Recommended next step: open the **{tab}** tab from the sidebar.")

        if st.session_state.get("recommended_next_tabs"):
            st.markdown("### ✅ Suggested Path")
            for tab in st.session_state["recommended_next_tabs"]:
                st.markdown(f"- {tab}")

        pdf_buffer = create_pdf_buffer("Client Intake Routing Report", st.session_state["intake_result"])

        st.download_button(
            "📄 Download Client Intake Report",
            pdf_buffer,
            file_name="Client_Intake_Routing_Report.pdf"
        )


if __name__ == "__main__":
    run()