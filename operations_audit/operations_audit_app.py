import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_operations_prompt(
    workflow,
    bottleneck,
    tools_used,
    team_involved,
    current_process,
    desired_outcome,
    automation_level,
    priority_area,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in operations audit mode: structured, practical, systems-focused, and efficiency-driven.

Return this exact structure:

1. Operations Snapshot
2. Workflow Breakdown
3. Main Bottlenecks
4. Process Gaps
5. Tool / System Issues
6. Automation Opportunities
7. Team or Handoff Improvements
8. Recommended Streamlined Workflow
9. FYW Tool Match
10. Next Best Actions
11. Final Operations Insight

Workflow / Process:
{workflow}

Main Bottleneck:
{bottleneck}

Tools Currently Used:
{tools_used}

Team Involved:
{team_involved}

Current Process:
{current_process}

Desired Outcome:
{desired_outcome}

Automation Level:
{automation_level}

Priority Area:
{priority_area}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- AI CMO Engine
- Strategic Simulator
- KPI Tracker
- Forecasting
- Growth
- CRM
- CRM Dashboard
- Business Development
- Consulting Guide
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


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("⚙️ Operations Audit")
    st.caption("Evaluate workflows, bottlenecks, tools, handoffs, and automation opportunities inside the business.")

    st.sidebar.header("💡 Operations Audit Guide")
    st.sidebar.markdown("""
**What this tool does:**
- audits business workflows and internal processes
- identifies bottlenecks, gaps, and inefficiencies
- recommends better systems, tools, handoffs, and automation
- helps turn scattered operations into a cleaner workflow

**Best use:**
Use when your business feels slow, disorganized, repetitive, tool-heavy, or hard to manage.

**Pro Tip:** Operations are where growth either becomes scalable or starts breaking the business.
""")

    defaults = {
        "ops_workflow": "",
        "ops_bottleneck": "",
        "ops_tools": "",
        "ops_team": "",
        "ops_current_process": "",
        "ops_desired_outcome": "",
        "ops_optional_notes": "",
        "ops_automation_level": "Some automation needed",
        "ops_priority_area": "Workflow Efficiency",
        "ops_audit_result": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.button("✨ Autofill Example"):
        st.session_state["ops_workflow"] = "Client onboarding process"
        st.session_state["ops_bottleneck"] = (
            "The process is slow because intake, email follow-up, payment, documents, and scheduling are spread across too many tools."
        )
        st.session_state["ops_tools"] = (
            "Google Forms, Gmail, Google Sheets, Wix, Calendly, and manual notes."
        )
        st.session_state["ops_team"] = (
            "Mostly one person handling client intake, follow-up, scheduling, and tracking."
        )
        st.session_state["ops_current_process"] = (
            "A client fills out a form, then information is reviewed manually, emails are sent manually, and next steps are tracked in separate places."
        )
        st.session_state["ops_desired_outcome"] = (
            "Create a cleaner onboarding flow where intake, follow-up, scheduling, and tracking are connected and easier to manage."
        )
        st.session_state["ops_automation_level"] = "Some automation needed"
        st.session_state["ops_priority_area"] = "Client Onboarding"
        st.session_state["ops_optional_notes"] = (
            "The goal is to reduce manual work while keeping the client experience professional and personal."
        )

    st.markdown("### 📥 Operations Audit Input")

    workflow = st.text_area(
        "Workflow / Process to Audit",
        key="ops_workflow",
        height=100,
        placeholder="Example: client onboarding, lead follow-up, order fulfillment, content workflow, team handoff, CRM process."
    )

    bottleneck = st.text_area(
        "Main Bottleneck",
        key="ops_bottleneck",
        height=100,
        placeholder="What feels slow, messy, repetitive, or broken?"
    )

    col1, col2 = st.columns(2)

    with col1:
        automation_level = st.selectbox(
            "Automation Need",
            [
                "No automation needed",
                "Some automation needed",
                "Heavy automation needed",
                "Not sure yet"
            ],
            key="ops_automation_level"
        )

    with col2:
        priority_area = st.selectbox(
            "Priority Area",
            [
                "Workflow Efficiency",
                "Client Onboarding",
                "Lead Follow-Up",
                "Team Handoff",
                "CRM / Data Tracking",
                "Fulfillment / Delivery",
                "Scheduling",
                "Reporting / KPIs",
                "Customer Experience"
            ],
            key="ops_priority_area"
        )

    tools_used = st.text_area(
        "Tools Currently Used",
        key="ops_tools",
        height=90,
        placeholder="Example: Google Sheets, Gmail, Wix, Trello, Notion, Bitrix24, Calendly, Zapier, Make."
    )

    team_involved = st.text_area(
        "Team / People Involved",
        key="ops_team",
        height=90,
        placeholder="Who touches this workflow?"
    )

    current_process = st.text_area(
        "Current Process",
        key="ops_current_process",
        height=110,
        placeholder="Describe how the process works now, step by step if possible."
    )

    desired_outcome = st.text_area(
        "Desired Outcome",
        key="ops_desired_outcome",
        height=100,
        placeholder="What should this process look like when improved?"
    )

    optional_notes = st.text_area(
        "Optional Notes",
        key="ops_optional_notes",
        height=90,
        placeholder="Add any details about budget, timeline, software limitations, staff, client experience, or recurring problems."
    )

    if st.button("🚀 Generate Operations Audit"):
        required = [
            workflow.strip(),
            bottleneck.strip(),
            current_process.strip(),
            desired_outcome.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main operations fields before generating.")
        else:
            try:
                with st.spinner("Auditing operations and building improvement plan..."):
                    prompt = build_operations_prompt(
                        workflow=workflow,
                        bottleneck=bottleneck,
                        tools_used=tools_used,
                        team_involved=team_involved,
                        current_process=current_process,
                        desired_outcome=desired_outcome,
                        automation_level=automation_level,
                        priority_area=priority_area,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in operations audit mode: systems-focused, practical, "
                                    "clear, process-oriented, and focused on efficiency, handoffs, automation, and execution."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.75,
                    )

                    output = response.choices[0].message.content
                    st.session_state["ops_audit_result"] = output

                    try:
                        save_data("Operations_Audit", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Workflow": workflow,
                            "Bottleneck": bottleneck,
                            "Tools_Used": tools_used,
                            "Team_Involved": team_involved,
                            "Current_Process": current_process,
                            "Desired_Outcome": desired_outcome,
                            "Automation_Level": automation_level,
                            "Priority_Area": priority_area,
                            "Optional_Notes": optional_notes,
                            "Audit_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Operations audit generated.")
                st.subheader("⚙️ Operations Audit Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("ops_audit_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Operations Audit Report", st.session_state["ops_audit_result"])

        st.download_button(
            "📄 Download Operations Audit Report",
            pdf_buffer,
            file_name="Operations_Audit_Report.pdf"
        )


if __name__ == "__main__":
    run()