import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


AI_MODEL = "gpt-4o"


def create_pdf_buffer(title, output):
    buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 40, title)

    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")

    text = pdf.beginText(50, height - 90)
    text.setFont("Helvetica", 9)

    y = height - 90

    for line in output.split("\n"):
        if y < 50:
            pdf.drawText(text)
            pdf.showPage()
            text = pdf.beginText(50, height - 50)
            text.setFont("Helvetica", 9)
            y = height - 50

        text.textLine(line[:120])
        y -= 11

    pdf.drawText(text)
    pdf.save()
    buffer.seek(0)
    return buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🌐 Network Deployment Engine")
    st.caption("Activate your existing network into a structured mission-based execution plan.")

    st.sidebar.header("🌐 Network Deployment Guide")
    st.sidebar.markdown("""
**What this tool does:**
- Activates people you already know
- Organizes your network around a specific goal
- Creates a Power Circle breakdown
- Identifies who to contact first
- Builds outreach messages and a 7-day action plan

**This is not:**
- CRM
- Network discovery
- Find Where You Win
- General business strategy

**Best use:**
Use when you already have people, contacts, groups, or access points — but need a smart deployment order.
""")

    defaults = {
        "nde_goal": "",
        "nde_objective": "",
        "nde_connections": "",
        "nde_resources": "",
        "nde_obstacles": "",
        "nde_timeline": "",
        "nde_support": "Advice, promotion, collaboration, referrals, warm introductions",
        "nde_output": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["nde_goal"] = "Launch a new premium consulting offer for small business owners."
        st.session_state["nde_objective"] = "Launch, grow visibility, gain referrals, and create early partnership conversations."
        st.session_state["nde_connections"] = "Local entrepreneurs, church leaders, nonprofit contacts, past design clients, cleaning business customers, social media followers, and business owners with community reach."
        st.session_state["nde_resources"] = "Promotion, referrals, testimonials, business feedback, warm introductions, content sharing, and possible collaboration partners."
        st.session_state["nde_obstacles"] = "Limited visibility, unclear outreach order, uncertainty about who to contact first, and needing a stronger message."
        st.session_state["nde_timeline"] = "7 days for first activation wave and 30 days for momentum."
        st.session_state["nde_support"] = "Advice, promotion, collaboration, referrals, warm introductions, credibility support"

    st.markdown("### 📥 Deployment Inputs")

    goal = st.text_area("Current Goal or Mission", key="nde_goal", height=100)

    objective = st.text_area(
        "What Are You Trying to Achieve? — launch, growth, partnership, funding, visibility, etc.",
        key="nde_objective",
        height=90
    )

    connections = st.text_area(
        "Known Connections or Types of People You Have Access To",
        key="nde_connections",
        height=120
    )

    resources = st.text_area(
        "Skills or Resources Needed",
        key="nde_resources",
        height=100
    )

    obstacles = st.text_area(
        "Current Obstacles",
        key="nde_obstacles",
        height=100
    )

    col1, col2 = st.columns(2)

    with col1:
        timeline = st.text_input("Timeline", key="nde_timeline")

    with col2:
        support = st.text_input(
            "Type of Support Needed",
            key="nde_support"
        )

    required = goal.strip() and objective.strip() and connections.strip() and timeline.strip()

    st.divider()

    if st.button("🌐 Generate Network Deployment Plan"):
        if not required:
            st.warning("Please complete Goal, Objective, Known Connections, and Timeline first.")
        else:
            with st.spinner("Building your network deployment plan..."):
                prompt = f"""
Act as Rain Intelligence inside the Find Your Way AI Consulting Suite.

You are running the Network Deployment Engine.

Purpose:
Turn the user's existing network into a structured, actionable deployment plan for a specific goal, mission, or business objective.

Important boundaries:
- This is NOT CRM.
- This is NOT a networking discovery tool.
- This is NOT Network Builder.
- This is NOT Find Where You Win.
- Do not tell the user to generally network.
- Assume they already have access to people.
- Focus only on activation, order, role assignment, and execution.

Tone:
Strategic, direct, execution-focused, premium consulting style.

User Inputs:
Current Goal or Mission: {goal}
What They Are Trying to Achieve: {objective}
Known Connections / People Access: {connections}
Skills or Resources Needed: {resources}
Current Obstacles: {obstacles}
Timeline: {timeline}
Type of Support Needed: {support}

Return a polished client-ready report with these sections:

1. Mission Summary
Summarize the mission clearly and directly.

2. Power Circle Breakdown
Break the user's network into activation roles:
- Connector
- Expert
- Builder
- Promoter
- Advisor
- Resource Holder

Explain what each role should do in this mission.

3. Key People to Activate
Identify the types of people the user should activate first based on their current network.

4. Missing Roles or Gaps
Explain what support appears missing, weak, or underdeveloped.

5. Deployment Order
Give a clear contact order:
- First
- Second
- Third
- Fourth
- Fifth

Explain why each group comes in that order.

6. Outreach Message Suggestions
Write 3 polished message templates:
- Soft relationship-based message
- Direct collaboration message
- Referral / introduction request message

7. Collaboration Strategy
Explain how to turn conversations into action without sounding desperate, scattered, or unclear.

8. 7-Day Network Action Plan
Give a day-by-day action plan for the next 7 days.

9. Final Execution Note
End with one direct instruction on what the user should do first.
"""

                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Rain Intelligence, a premium strategic execution advisor for Find Your Way Network Marketing Consultants."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.72,
                )

                st.session_state["nde_output"] = response.choices[0].message.content

                try:
                    save_data("Network_Deployment_Engine", {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "User_Role": st.session_state.get("user_role", "guest"),
                        "Goal": goal,
                        "Objective": objective,
                        "Connections": connections,
                        "Resources_Needed": resources,
                        "Obstacles": obstacles,
                        "Timeline": timeline,
                        "Support_Needed": support,
                        "AI_Output": st.session_state["nde_output"],
                    })
                    st.success("✅ Network Deployment Plan generated and saved.")
                except Exception as save_error:
                    st.warning(f"Plan generated, but Google Sheets save had an issue: {save_error}")

    if st.session_state["nde_output"]:
        st.subheader("✅ Network Deployment Plan")
        st.markdown(st.session_state["nde_output"])

        pdf_buffer = create_pdf_buffer(
            "Network Deployment Engine Report",
            st.session_state["nde_output"]
        )

        st.download_button(
            "📄 Download Network Deployment Plan",
            pdf_buffer,
            file_name="Network_Deployment_Engine_Report.pdf"
        )


if __name__ == "__main__":
    run()