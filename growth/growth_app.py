import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_growth_prompt(
    growth_goal,
    business_stage,
    growth_area,
    current_position,
    biggest_constraint,
    available_assets,
    target_audience,
    timeline,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in growth strategy mode: strategic, practical, commercially sharp, and execution-focused.

Return this exact structure:

1. Growth Snapshot
2. Current Position Read
3. Main Growth Constraint
4. Best Growth Opportunities
5. Strategic Growth Path
6. Audience / Market Expansion Angle
7. Assets to Leverage
8. 30-Day Growth Plan
9. FYW Tool Match
10. KPI Suggestions
11. Next Best Actions
12. Final Growth Insight

Growth Goal:
{growth_goal}

Business Stage:
{business_stage}

Growth Area:
{growth_area}

Current Position:
{current_position}

Biggest Constraint:
{biggest_constraint}

Available Assets:
{available_assets}

Target Audience:
{target_audience}

Timeline:
{timeline}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- AI CMO Engine
- Strategic Simulator
- KPI Tracker
- Forecasting
- Marketing Hub
- Marketing Planner
- Lead Generation
- Business Development
- CRM Dashboard
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

    st.title("📈 Growth Strategy")
    st.caption("Build a focused growth path based on your current position, constraints, audience, and available assets.")

    st.sidebar.header("💡 Growth Strategy Guide")
    st.sidebar.markdown("""
**What this tool does:**
- identifies realistic growth opportunities
- clarifies what is holding growth back
- turns current assets into a growth path
- creates a practical 30-day growth plan
- recommends KPIs to track progress

**Best use:**
Use after AI CMO Engine, Business Development, Marketing Planner, or Forecasting when you need a clear growth direction.

**Pro Tip:** Growth is not just doing more. It is choosing the right leverage point and executing consistently.
""")

    defaults = {
        "growth_goal": "",
        "growth_current_position": "",
        "growth_biggest_constraint": "",
        "growth_available_assets": "",
        "growth_target_audience": "",
        "growth_optional_notes": "",
        "growth_business_stage": "Growing",
        "growth_area": "Revenue Growth",
        "growth_timeline": "Next 30 days",
        "growth_result": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.button("✨ Autofill Suggestion"):
        st.session_state["growth_goal"] = (
            "Increase consistent client flow and convert more interested leads into paid Elite access or consulting clients."
        )
        st.session_state["growth_business_stage"] = "Growing"
        st.session_state["growth_area"] = "Revenue Growth"
        st.session_state["growth_current_position"] = (
            "The business has a website, AI tools, service structure, InterNetwork concept, and multiple offers, "
            "but needs more consistent visibility and conversion flow."
        )
        st.session_state["growth_biggest_constraint"] = (
            "The biggest constraint is turning attention into a simple path that leads people from interest to action."
        )
        st.session_state["growth_available_assets"] = (
            "Website pages, AI Consulting Suite, email flows, lead magnets, InterNetwork, service pages, social content, and business frameworks."
        )
        st.session_state["growth_target_audience"] = (
            "Small business owners, entrepreneurs, service providers, creators, and people who need structure, strategy, and growth support."
        )
        st.session_state["growth_timeline"] = "Next 30 days"
        st.session_state["growth_optional_notes"] = (
            "The growth plan should focus on clarity, traffic, lead capture, and upgrades without overcomplicating the system."
        )

    st.markdown("### 📥 Growth Strategy Input")

    growth_goal = st.text_area(
        "Growth Goal",
        key="growth_goal",
        height=100,
        placeholder="What are you trying to grow, increase, improve, or scale?"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        business_stage = st.selectbox(
            "Business Stage",
            ["Startup", "Growing", "Established", "Scaling"],
            key="growth_business_stage"
        )

    with col2:
        growth_area = st.selectbox(
            "Growth Area",
            [
                "Revenue Growth",
                "Lead Growth",
                "Audience Growth",
                "Client Retention",
                "Visibility Growth",
                "Operational Scale",
                "Network / Partnership Growth",
                "Product / Offer Expansion"
            ],
            key="growth_area"
        )

    with col3:
        timeline = st.selectbox(
            "Timeline",
            ["Next 7 days", "Next 30 days", "Next 90 days", "Next 6 months", "Next 12 months"],
            key="growth_timeline"
        )

    current_position = st.text_area(
        "Current Position",
        key="growth_current_position",
        height=100,
        placeholder="Where are you now? What exists already?"
    )

    biggest_constraint = st.text_area(
        "Biggest Constraint",
        key="growth_biggest_constraint",
        height=100,
        placeholder="What is holding growth back right now?"
    )

    available_assets = st.text_area(
        "Available Assets",
        key="growth_available_assets",
        height=100,
        placeholder="What tools, offers, content, relationships, systems, or audience do you already have?"
    )

    target_audience = st.text_area(
        "Target Audience",
        key="growth_target_audience",
        height=100,
        placeholder="Who are you trying to reach, attract, serve, or convert?"
    )

    optional_notes = st.text_area(
        "Optional Notes",
        key="growth_optional_notes",
        height=90,
        placeholder="Add context about budget, team, timeline, current marketing, market conditions, or goals."
    )

    if st.button("🚀 Generate Growth Strategy"):
        required = [
            growth_goal.strip(),
            current_position.strip(),
            biggest_constraint.strip(),
            available_assets.strip(),
            target_audience.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main growth fields before generating.")
        else:
            try:
                with st.spinner("Building growth strategy..."):
                    prompt = build_growth_prompt(
                        growth_goal=growth_goal,
                        business_stage=business_stage,
                        growth_area=growth_area,
                        current_position=current_position,
                        biggest_constraint=biggest_constraint,
                        available_assets=available_assets,
                        target_audience=target_audience,
                        timeline=timeline,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in growth strategy mode: strategic, practical, "
                                    "commercially sharp, and focused on execution, leverage, and measurable progress."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["growth_result"] = output

                    try:
                        save_data("Growth", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Growth_Goal": growth_goal,
                            "Business_Stage": business_stage,
                            "Growth_Area": growth_area,
                            "Timeline": timeline,
                            "Current_Position": current_position,
                            "Biggest_Constraint": biggest_constraint,
                            "Available_Assets": available_assets,
                            "Target_Audience": target_audience,
                            "Optional_Notes": optional_notes,
                            "Growth_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Growth strategy generated.")
                st.subheader("📈 Growth Strategy Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("growth_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Growth Strategy Report", st.session_state["growth_result"])

        st.download_button(
            "📄 Download Growth Strategy Report",
            pdf_buffer,
            file_name="Growth_Strategy_Report.pdf"
        )


if __name__ == "__main__":
    run()