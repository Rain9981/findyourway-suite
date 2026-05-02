import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


AI_MODEL = "gpt-4o"


def build_campaign_prompt(
    business_name,
    offer,
    audience,
    campaign_goal,
    platforms,
    tone,
    emotional_trigger,
    campaign_length,
    cta,
    budget_level,
    visual_style,
    lead_magnet_goal,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in elite CMO campaign production mode.

You are a senior marketing strategist, direct-response copywriter, brand psychologist, paid ads strategist, and content planner.

Create a complete campaign asset package that is practical, copy-paste ready, and emotionally persuasive.

Return the response in this exact structure:

1. Campaign Snapshot
2. Audience Psychology
3. Core Campaign Message
4. 21-Day Content Calendar
   For each day include:
   - Day
   - Platform Best Fit
   - Post Type
   - Hook
   - Caption / Post Copy
   - CTA
   - Visual or Design Idea
5. Lead Magnet Ideas
   Include 7 ideas with:
   - Title
   - Format
   - Why It Converts
   - CTA
6. 10 Paid Ad Variations
   For each ad include:
   - Platform Best Fit
   - Headline
   - Primary Text
   - CTA
   - Visual Direction
   - Funnel Stage
7. 5 Short-Form Video Ideas
   For each video include:
   - Concept
   - 3-Second Hook
   - Script Outline
   - Visual Style
   - CTA
8. Campaign Posting Strategy
9. Messaging Risks to Avoid
10. Repurposing Ideas
11. FYW Tool Match
12. Final CMO Campaign Insight

Business Name:
{business_name}

Offer / Service:
{offer}

Target Audience:
{audience}

Campaign Goal:
{campaign_goal}

Platforms:
{platforms}

Tone:
{tone}

Emotional Trigger:
{emotional_trigger}

Campaign Length:
{campaign_length}

Main CTA:
{cta}

Budget Level:
{budget_level}

Visual Style:
{visual_style}

Lead Magnet Goal:
{lead_magnet_goal}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Marketing Hub
- Marketing Planner
- Email Marketing
- Lead Generation
- AI CMO Engine
- Strategic Simulator
- Sentiment Analysis
- KPI Tracker
"""


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

    st.title("📢 Campaign Engine")
    st.caption("Generate 21 days of content, social copy, visual ideas, paid ads, video ideas, and lead magnets.")

    st.sidebar.header("💡 Campaign Engine Guide")
    st.sidebar.markdown("""
**What this tool does:**
- creates a 21-day campaign content plan
- writes copy-paste ready captions
- gives visual/design ideas
- generates paid ad variations
- creates short-form video ideas
- suggests lead magnets

**Best use:**
Use after Marketing Hub and Marketing Planner when you are ready to produce actual campaign assets.

**Pro Tip:** The more specific your audience, offer, and emotional trigger, the stronger the output.
""")

    defaults = {
        "ce_business_name": "",
        "ce_offer": "",
        "ce_audience": "",
        "ce_campaign_goal": "",
        "ce_platforms": "Facebook, Instagram, TikTok, Google",
        "ce_tone": "Professional / Persuasive",
        "ce_emotional_trigger": "Clarity and confidence",
        "ce_campaign_length": "21 days",
        "ce_cta": "",
        "ce_budget_level": "Low budget",
        "ce_visual_style": "Modern, premium, clean",
        "ce_lead_magnet_goal": "",
        "ce_optional_notes": "",
        "campaign_engine_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["ce_business_name"] = "Find Your Way Network Marketing Consultants"
        st.session_state["ce_offer"] = "Elite access to the AI Consulting Suite with tools for strategy, marketing, CRM, growth, and performance tracking."
        st.session_state["ce_audience"] = "Small business owners, entrepreneurs, service providers, and creators who feel scattered and need structure, strategy, and smarter execution."
        st.session_state["ce_campaign_goal"] = "Increase awareness and drive upgrades into Elite access."
        st.session_state["ce_platforms"] = "Facebook, Instagram, TikTok, LinkedIn, Google Display"
        st.session_state["ce_tone"] = "Professional / Persuasive"
        st.session_state["ce_emotional_trigger"] = "Clarity and confidence"
        st.session_state["ce_campaign_length"] = "21 days"
        st.session_state["ce_cta"] = "Upgrade to Elite Access or start with Client Intake."
        st.session_state["ce_budget_level"] = "Low budget"
        st.session_state["ce_visual_style"] = "Black, burgundy, gold, modern AI consulting command center aesthetic."
        st.session_state["ce_lead_magnet_goal"] = "Collect qualified leads interested in business growth, AI tools, and consulting support."
        st.session_state["ce_optional_notes"] = "Campaign should feel premium, intelligent, and clear without overwhelming the audience."

    st.markdown("### 📥 Campaign Parameters")

    business_name = st.text_input("Business Name", key="ce_business_name")

    offer = st.text_area("Offer / Service", key="ce_offer", height=100)
    audience = st.text_area("Target Audience", key="ce_audience", height=100)
    campaign_goal = st.text_area("Campaign Goal", key="ce_campaign_goal", height=90)

    col1, col2 = st.columns(2)

    with col1:
        platforms = st.text_area("Platforms", key="ce_platforms", height=90)
        tone = st.selectbox(
            "Tone",
            [
                "Professional / Persuasive",
                "Luxury / Premium",
                "Bold / Direct",
                "Warm / Relatable",
                "Educational / Helpful",
                "Visionary / Inspirational",
                "Urgent / Conversion-Focused"
            ],
            key="ce_tone"
        )

        campaign_length = st.selectbox(
            "Campaign Length",
            ["7 days", "14 days", "21 days", "30 days"],
            key="ce_campaign_length"
        )

    with col2:
        emotional_trigger = st.selectbox(
            "Emotional Trigger",
            [
                "Clarity and confidence",
                "Fear of staying stuck",
                "Desire for transformation",
                "Trust and credibility",
                "Urgency and opportunity",
                "Luxury and status",
                "Relief from overwhelm",
                "Belonging and community"
            ],
            key="ce_emotional_trigger"
        )

        budget_level = st.selectbox(
            "Budget Level",
            ["No budget", "Low budget", "Moderate budget", "High budget"],
            key="ce_budget_level"
        )

        visual_style = st.text_area("Visual Style", key="ce_visual_style", height=90)

    cta = st.text_area("Main CTA", key="ce_cta", height=80)
    lead_magnet_goal = st.text_area("Lead Magnet Goal", key="ce_lead_magnet_goal", height=80)
    optional_notes = st.text_area("Optional Notes", key="ce_optional_notes", height=100)

    if st.button("🚀 Generate Campaign Assets"):
        required = [
            business_name.strip(),
            offer.strip(),
            audience.strip(),
            campaign_goal.strip(),
            cta.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main campaign fields before generating.")
        else:
            try:
                with st.spinner("Generating campaign assets..."):
                    prompt = build_campaign_prompt(
                        business_name=business_name,
                        offer=offer,
                        audience=audience,
                        campaign_goal=campaign_goal,
                        platforms=platforms,
                        tone=tone,
                        emotional_trigger=emotional_trigger,
                        campaign_length=campaign_length,
                        cta=cta,
                        budget_level=budget_level,
                        visual_style=visual_style,
                        lead_magnet_goal=lead_magnet_goal,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model=AI_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in elite CMO campaign production mode: "
                                    "strategic, persuasive, conversion-focused, creative, and practical."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.85,
                    )

                    output = response.choices[0].message.content
                    st.session_state["campaign_engine_result"] = output

                    try:
                        save_data("Campaign_Engine", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Business_Name": business_name,
                            "Offer": offer,
                            "Audience": audience,
                            "Campaign_Goal": campaign_goal,
                            "Platforms": platforms,
                            "Tone": tone,
                            "Emotional_Trigger": emotional_trigger,
                            "Campaign_Length": campaign_length,
                            "CTA": cta,
                            "Budget_Level": budget_level,
                            "Visual_Style": visual_style,
                            "Lead_Magnet_Goal": lead_magnet_goal,
                            "Optional_Notes": optional_notes,
                            "Campaign_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Campaign assets generated.")
                st.subheader("📢 Campaign Asset Package")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("campaign_engine_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Campaign Engine Report", st.session_state["campaign_engine_result"])

        st.download_button(
            "📄 Download Campaign Report",
            pdf_buffer,
            file_name="Campaign_Engine_Report.pdf"
        )


if __name__ == "__main__":
    run()