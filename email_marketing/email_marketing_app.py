import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_email_prompt(
    campaign_goal,
    target_audience,
    offer,
    pain_point,
    desired_action,
    email_type,
    tone,
    urgency_level,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in conversion-focused email marketing mode: persuasive, clear, ethical, psychologically aware, and action-oriented.

You are helping create or refine a marketing email that builds trust, speaks to the audience's need, and moves them toward action.

Return the response in this exact structure:

1. Campaign Snapshot
2. Audience Psychology
3. Subject Line Options
4. Preview Text Options
5. Opening Hook
6. Email Body
7. Call To Action
8. Follow-Up Email Idea
9. Risk / Weakness to Avoid
10. FYW Tool Match
11. Final Email Strategy Insight

Campaign Goal:
{campaign_goal}

Target Audience:
{target_audience}

Offer:
{offer}

Audience Pain Point:
{pain_point}

Desired Action:
{desired_action}

Email Type:
{email_type}

Tone:
{tone}

Urgency Level:
{urgency_level}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Marketing Hub
- Lead Generation
- Sentiment Analysis
- AI CMO Engine
- Strategic Simulator
- Brand Positioning
- Consulting Guide
"""


def create_pdf_buffer(title, output):
    pdf_buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 40, title)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")

    text = pdf.beginText(50, height - 90)
    text.setFont("Helvetica", 10)

    y_position = height - 90
    for line in output.split("\n"):
        if y_position < 50:
            pdf.drawText(text)
            pdf.showPage()
            text = pdf.beginText(50, height - 50)
            text.setFont("Helvetica", 10)
            y_position = height - 50
        text.textLine(line[:110])
        y_position -= 12

    pdf.drawText(text)
    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("📬 Email Marketing")
    st.caption("Create strategic marketing emails that connect with the audience, build trust, and drive action.")

    st.sidebar.header("💡 Email Marketing Guide")
    st.sidebar.markdown("""
**What this tool does:**
- creates promotional, welcome, follow-up, and re-engagement emails
- improves campaign clarity, tone, and conversion strength
- adds subject lines, preview text, CTA, and follow-up ideas
- helps connect email strategy to your larger FYW growth system

**What to enter:**
- Campaign goal
- Target audience
- Offer or service
- Pain point
- Desired action

**Best use:**
Use this after Lead Generation, Marketing Hub, or Sentiment Analysis when you need a stronger email message.

**Pro Tip:** A strong email does not just explain the offer. It speaks to the reader's current problem and gives them a clear next step.
""")

    defaults = {
        "email_campaign_goal": "",
        "email_target_audience": "",
        "email_offer": "",
        "email_pain_point": "",
        "email_desired_action": "",
        "email_optional_notes": "",
        "email_type": "Promotional Email",
        "email_tone": "Professional / Persuasive",
        "email_urgency": "Moderate",
        "email_marketing_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["email_campaign_goal"] = (
            "Promote the Find Your Way Elite access tier to past leads who showed interest but have not upgraded yet."
        )
        st.session_state["email_target_audience"] = (
            "Small business owners, entrepreneurs, and service providers who need better strategy, structure, and growth tools."
        )
        st.session_state["email_offer"] = (
            "Elite access to the Find Your Way AI Consulting Suite, including tools like AI CMO Engine, Strategic Simulator, Lead Generation, Marketing Hub, and Growth support."
        )
        st.session_state["email_pain_point"] = (
            "They have ideas and ambition, but they feel scattered, unsure what to focus on next, and need a clearer system to grow."
        )
        st.session_state["email_desired_action"] = (
            "Click the button to upgrade to Elite access or revisit the subscription page."
        )
        st.session_state["email_type"] = "Promotional Email"
        st.session_state["email_tone"] = "Professional / Persuasive"
        st.session_state["email_urgency"] = "Moderate"
        st.session_state["email_optional_notes"] = (
            "The email should feel helpful and strategic, not pushy. It should make Elite feel like the smart next step."
        )

    st.markdown("### 📥 Email Campaign Input")

    campaign_goal = st.text_area(
        "Campaign Goal",
        key="email_campaign_goal",
        height=100,
        placeholder="What is this email trying to accomplish?"
    )

    target_audience = st.text_area(
        "Target Audience",
        key="email_target_audience",
        height=100,
        placeholder="Who is this email for?"
    )

    offer = st.text_area(
        "Offer / Service",
        key="email_offer",
        height=100,
        placeholder="What are you promoting, offering, or explaining?"
    )

    pain_point = st.text_area(
        "Audience Pain Point",
        key="email_pain_point",
        height=100,
        placeholder="What problem, desire, hesitation, or frustration is the reader dealing with?"
    )

    desired_action = st.text_area(
        "Desired Action",
        key="email_desired_action",
        height=90,
        placeholder="What should the reader do next?"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        email_type = st.selectbox(
            "Email Type",
            [
                "Promotional Email",
                "Welcome Email",
                "Follow-Up Email",
                "Re-Engagement Email",
                "Lead Magnet Delivery",
                "Announcement Email",
                "Nurture Email",
                "Consultation Invitation"
            ],
            key="email_type"
        )

    with col2:
        tone = st.selectbox(
            "Tone",
            [
                "Professional / Persuasive",
                "Warm / Encouraging",
                "Luxury / Premium",
                "Direct / Action-Focused",
                "Educational / Helpful",
                "Urgent / Time-Sensitive",
                "Visionary / Inspirational"
            ],
            key="email_tone"
        )

    with col3:
        urgency_level = st.selectbox(
            "Urgency Level",
            [
                "Low",
                "Moderate",
                "High"
            ],
            key="email_urgency"
        )

    optional_notes = st.text_area(
        "Optional Notes",
        key="email_optional_notes",
        height=100,
        placeholder="Add context about brand voice, audience relationship, deadline, link, offer details, or past communication."
    )

    if st.button("🚀 Generate Email Campaign"):
        required = [
            campaign_goal.strip(),
            target_audience.strip(),
            offer.strip(),
            pain_point.strip(),
            desired_action.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main email fields before generating.")
        else:
            try:
                with st.spinner("Writing your email marketing campaign..."):
                    prompt = build_email_prompt(
                        campaign_goal=campaign_goal,
                        target_audience=target_audience,
                        offer=offer,
                        pain_point=pain_point,
                        desired_action=desired_action,
                        email_type=email_type,
                        tone=tone,
                        urgency_level=urgency_level,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in email marketing mode: persuasive, clear, "
                                    "strategic, ethical, psychologically aware, and conversion-focused."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["email_marketing_result"] = output

                    try:
                        save_data("Email_Marketing", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Campaign_Goal": campaign_goal,
                            "Target_Audience": target_audience,
                            "Offer": offer,
                            "Pain_Point": pain_point,
                            "Desired_Action": desired_action,
                            "Email_Type": email_type,
                            "Tone": tone,
                            "Urgency_Level": urgency_level,
                            "Optional_Notes": optional_notes,
                            "GPT_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Email generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Email campaign generated.")
                st.subheader("📬 Email Marketing Campaign")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("email_marketing_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Email Marketing Campaign Report", st.session_state["email_marketing_result"])

        st.download_button(
            "📄 Download Email Marketing Report",
            data=pdf_buffer,
            file_name="Email_Marketing_Report.pdf"
        )


if __name__ == "__main__":
    run()