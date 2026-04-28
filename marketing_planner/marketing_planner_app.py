import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_marketing_planner_prompt(campaign_name, goal, audience, offer, channels, timeline, budget_level, content_frequency, success_metrics, optional_notes):
    return f"""
Act as Rain Intelligence in campaign planning mode: structured, practical, strategic, and execution-focused.

Return this exact structure:

1. Campaign Plan Snapshot
2. Campaign Objective
3. Audience Targeting
4. Channel Plan
5. Content Plan
6. Weekly Execution Timeline
7. CTA Strategy
8. Success Metrics
9. Risk / Bottleneck Warnings
10. FYW Tool Match
11. Next Best Actions
12. Final Campaign Planning Insight

Campaign Name:
{campaign_name}

Goal:
{goal}

Audience:
{audience}

Offer:
{offer}

Channels:
{channels}

Timeline:
{timeline}

Budget Level:
{budget_level}

Content Frequency:
{content_frequency}

Success Metrics:
{success_metrics}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Marketing Hub
- Email Marketing
- Lead Generation
- Sentiment Analysis
- AI CMO Engine
- Strategic Simulator
- KPI Tracker
- Forecasting
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

    st.title("📅 Marketing Planner")
    st.caption("Turn a campaign idea into a structured execution plan with timeline, channels, content, and success metrics.")

    st.sidebar.header("💡 Marketing Planner Guide")
    st.sidebar.markdown("""
**What this tool does:**
- turns marketing ideas into an execution plan
- organizes campaign channels, timeline, and content
- identifies success metrics and bottlenecks
- helps move from strategy into action

**Best use:**
Use after Marketing Hub when your message is clear and you need a practical campaign plan.

**Pro Tip:** Marketing Hub shapes the message. Marketing Planner builds the schedule and execution path.
""")

    defaults = {
        "mp_campaign_name": "",
        "mp_goal": "",
        "mp_audience": "",
        "mp_offer": "",
        "mp_channels": "",
        "mp_success_metrics": "",
        "mp_optional_notes": "",
        "mp_timeline": "30 days",
        "mp_budget_level": "Low budget",
        "mp_content_frequency": "3 posts per week",
        "marketing_planner_result": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.button("✨ Autofill Example"):
        st.session_state["mp_campaign_name"] = "Elite Access Launch Campaign"
        st.session_state["mp_goal"] = "Increase upgrades to Elite access in the AI Consulting Suite."
        st.session_state["mp_audience"] = "Business owners and entrepreneurs who need clearer strategy, tools, and execution support."
        st.session_state["mp_offer"] = "Elite subscription access with AI CMO Engine, Strategic Simulator, Lead Generation, Marketing Hub, and Growth tools."
        st.session_state["mp_channels"] = "Website, email, social media, direct outreach, and InterNetwork page."
        st.session_state["mp_timeline"] = "30 days"
        st.session_state["mp_budget_level"] = "Low budget"
        st.session_state["mp_content_frequency"] = "3 posts per week"
        st.session_state["mp_success_metrics"] = "Subscription clicks, upgrades, email replies, booked calls, and engagement."
        st.session_state["mp_optional_notes"] = "Campaign should make Elite feel like the smart starting point for serious builders."

    st.markdown("### 📥 Marketing Planner Input")

    campaign_name = st.text_input("Campaign Name", key="mp_campaign_name")
    goal = st.text_area("Campaign Goal", key="mp_goal", height=90)
    audience = st.text_area("Target Audience", key="mp_audience", height=90)
    offer = st.text_area("Offer / Service", key="mp_offer", height=90)
    channels = st.text_area("Campaign Channels", key="mp_channels", height=90)

    col1, col2, col3 = st.columns(3)

    with col1:
        timeline = st.selectbox("Timeline", ["7 days", "14 days", "30 days", "60 days", "90 days"], key="mp_timeline")

    with col2:
        budget_level = st.selectbox("Budget Level", ["No budget", "Low budget", "Moderate budget", "High budget"], key="mp_budget_level")

    with col3:
        content_frequency = st.selectbox(
            "Content Frequency",
            ["1 post per week", "3 posts per week", "5 posts per week", "Daily", "Multiple times per day"],
            key="mp_content_frequency"
        )

    success_metrics = st.text_area("Success Metrics", key="mp_success_metrics", height=90)
    optional_notes = st.text_area("Optional Notes", key="mp_optional_notes", height=90)

    if st.button("🚀 Generate Marketing Plan"):
        required = [campaign_name.strip(), goal.strip(), audience.strip(), offer.strip(), channels.strip()]
        if not all(required):
            st.warning("⚠️ Please complete the main campaign fields before generating.")
        else:
            try:
                with st.spinner("Building marketing campaign plan..."):
                    prompt = build_marketing_planner_prompt(
                        campaign_name, goal, audience, offer, channels, timeline,
                        budget_level, content_frequency, success_metrics, optional_notes
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are Rain Intelligence in campaign planning mode: structured, strategic, practical, and execution-focused."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.75,
                    )

                    output = response.choices[0].message.content
                    st.session_state["marketing_planner_result"] = output

                    try:
                        save_data("Marketing_Planner", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Campaign_Name": campaign_name,
                            "Goal": goal,
                            "Audience": audience,
                            "Offer": offer,
                            "Channels": channels,
                            "Timeline": timeline,
                            "Budget_Level": budget_level,
                            "Content_Frequency": content_frequency,
                            "Success_Metrics": success_metrics,
                            "Optional_Notes": optional_notes,
                            "Marketing_Plan": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Marketing plan generated.")
                st.subheader("📅 Marketing Campaign Plan")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("marketing_planner_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Marketing Planner Report", st.session_state["marketing_planner_result"])
        st.download_button("📄 Download Marketing Planner Report", pdf_buffer, file_name="Marketing_Planner_Report.pdf")


if __name__ == "__main__":
    run()