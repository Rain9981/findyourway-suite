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

    st.title("📢 Campaign Engine V3")
    st.caption("Generate campaign strategy, 21-day content, lead magnets, paid ads, video ideas, and a final CMO-level campaign report.")

    st.sidebar.header("💡 Campaign Engine Guide")
    st.sidebar.markdown("""
**What this tool does:**
- builds a campaign strategy
- creates a full 21-day content calendar
- generates lead magnet ideas
- creates 10 ads
- creates 5 video ideas
- combines everything into a polished campaign report

**Best use:**
Use after Marketing Hub and Marketing Planner.

**Pro Tip:** Generate each section first, then use the final report button to create the premium campaign document.
""")

    defaults = {
        "ce_business": "",
        "ce_offer": "",
        "ce_audience": "",
        "ce_goal": "",
        "ce_platforms": "Facebook, Instagram, TikTok, LinkedIn, Google",
        "ce_tone": "Professional / Persuasive",
        "ce_emotion": "Clarity and confidence",
        "ce_cta": "",
        "ce_budget": "Low budget",
        "ce_visual": "Modern, clean, premium",
        "ce_notes": "",
        "strategy_output": "",
        "content_output": "",
        "lead_output": "",
        "ads_output": "",
        "video_output": "",
        "full_report_output": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["ce_business"] = "Find Your Way Network Marketing Consultants"
        st.session_state["ce_offer"] = "Elite access to the AI Consulting Suite with tools for strategy, marketing, CRM, growth, and performance tracking."
        st.session_state["ce_audience"] = "Small business owners, entrepreneurs, service providers, and creators who feel scattered and need structure, strategy, and smarter execution."
        st.session_state["ce_goal"] = "Increase awareness and drive upgrades into Elite access."
        st.session_state["ce_platforms"] = "Facebook, Instagram, TikTok, LinkedIn, Google Display"
        st.session_state["ce_tone"] = "Professional / Persuasive"
        st.session_state["ce_emotion"] = "Clarity and confidence"
        st.session_state["ce_cta"] = "Upgrade to Elite Access or start with Client Intake."
        st.session_state["ce_budget"] = "Low budget"
        st.session_state["ce_visual"] = "Black, burgundy, gold, modern AI consulting command center aesthetic."
        st.session_state["ce_notes"] = "Campaign should feel premium, intelligent, and clear without overwhelming the audience."

    st.markdown("### 📥 Campaign Inputs")

    business = st.text_input("Business Name", key="ce_business")
    offer = st.text_area("Offer / Service", key="ce_offer", height=100)
    audience = st.text_area("Target Audience", key="ce_audience", height=100)
    goal = st.text_area("Campaign Goal", key="ce_goal", height=90)

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

        budget = st.selectbox(
            "Budget Level",
            ["No budget", "Low budget", "Moderate budget", "High budget"],
            key="ce_budget"
        )

    with col2:
        emotion = st.selectbox(
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
            key="ce_emotion"
        )

        visual = st.text_area("Visual Style", key="ce_visual", height=90)
        cta = st.text_area("Main CTA", key="ce_cta", height=90)

    notes = st.text_area("Optional Notes", key="ce_notes", height=100)

    required = business.strip() and offer.strip() and audience.strip() and goal.strip() and cta.strip()

    st.divider()
    st.markdown("## 🧠 Generate Campaign Sections")

    if st.button("🧠 Generate Campaign Strategy"):
        if not required:
            st.warning("Please complete Business, Offer, Audience, Goal, and CTA first.")
        else:
            with st.spinner("Generating campaign strategy..."):
                prompt = f"""
Act as Rain Intelligence in elite CMO strategy mode.

Create a campaign strategy for:

Business: {business}
Offer: {offer}
Audience: {audience}
Goal: {goal}
Platforms: {platforms}
Tone: {tone}
Emotional Trigger: {emotion}
CTA: {cta}
Budget: {budget}
Visual Style: {visual}
Notes: {notes}

Return:
1. Campaign Snapshot
2. Audience Psychology
3. Core Message
4. Funnel Strategy
5. Main Campaign Angle
6. Posting Strategy
7. Messaging Risks to Avoid
8. Final CMO Insight
"""
                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are Rain Intelligence, an elite CMO and campaign strategist."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.75,
                )
                st.session_state["strategy_output"] = response.choices[0].message.content

    if st.session_state["strategy_output"]:
        st.subheader("🧠 Campaign Strategy")
        st.markdown(st.session_state["strategy_output"])

    if st.button("📅 Generate Full 21-Day Content Calendar"):
        if not required:
            st.warning("Please complete Business, Offer, Audience, Goal, and CTA first.")
        else:
            with st.spinner("Generating full 21-day content calendar..."):
                prompt = f"""
Create a FULL 21-day content calendar.

Business: {business}
Offer: {offer}
Audience: {audience}
Goal: {goal}
Platforms: {platforms}
Tone: {tone}
Emotional Trigger: {emotion}
CTA: {cta}
Visual Style: {visual}

Rules:
- Do NOT skip days.
- Include exactly Day 1 through Day 21.
- Keep each day short enough to complete all days.
- Make captions copy-paste ready.

For each day include:
Day:
Platform Best Fit:
Post Type:
Hook:
Caption / Post Copy:
CTA:
Visual or Design Idea:
"""
                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a social media campaign strategist. Complete all 21 days without skipping."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                )
                st.session_state["content_output"] = response.choices[0].message.content

    if st.session_state["content_output"]:
        st.subheader("📅 21-Day Content Calendar")
        st.markdown(st.session_state["content_output"])

    if st.button("🎯 Generate Lead Magnet Ideas"):
        if not required:
            st.warning("Please complete Business, Offer, Audience, Goal, and CTA first.")
        else:
            with st.spinner("Generating lead magnet ideas..."):
                prompt = f"""
Create 7 lead magnet ideas for:

Business: {business}
Offer: {offer}
Audience: {audience}
Goal: {goal}
CTA: {cta}

For each include:
1. Title
2. Format
3. What problem it solves
4. Why it converts
5. CTA
6. Visual idea
"""
                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a lead generation strategist and offer architect."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                )
                st.session_state["lead_output"] = response.choices[0].message.content

    if st.session_state["lead_output"]:
        st.subheader("🎯 Lead Magnet Ideas")
        st.markdown(st.session_state["lead_output"])

    if st.button("📢 Generate 10 Paid Ads"):
        if not required:
            st.warning("Please complete Business, Offer, Audience, Goal, and CTA first.")
        else:
            with st.spinner("Generating 10 paid ads..."):
                prompt = f"""
Create exactly 10 paid ad variations.

Business: {business}
Offer: {offer}
Audience: {audience}
Goal: {goal}
Platforms: {platforms}
Tone: {tone}
Emotional Trigger: {emotion}
CTA: {cta}
Visual Style: {visual}

Rules:
- Include exactly Ad 1 through Ad 10.
- Do not skip any ad.
- Make each ad platform-ready.

For each ad include:
Ad Number:
Platform Best Fit:
Headline:
Primary Text:
CTA:
Visual Direction:
Funnel Stage:
"""
                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a paid ads strategist and direct-response copywriter. Complete all 10 ads."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                )
                st.session_state["ads_output"] = response.choices[0].message.content

    if st.session_state["ads_output"]:
        st.subheader("📢 10 Paid Ad Variations")
        st.markdown(st.session_state["ads_output"])

    if st.button("🎥 Generate 5 Video Ideas"):
        if not required:
            st.warning("Please complete Business, Offer, Audience, Goal, and CTA first.")
        else:
            with st.spinner("Generating video ideas..."):
                prompt = f"""
Create 5 short-form video ideas.

Business: {business}
Offer: {offer}
Audience: {audience}
Goal: {goal}
Tone: {tone}
Emotional Trigger: {emotion}
CTA: {cta}
Visual Style: {visual}

For each video include:
Video Number:
Concept:
3-Second Hook:
Script Outline:
Visual Style:
CTA:
Repurpose Idea:
"""
                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a short-form video strategist and campaign creative director."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                )
                st.session_state["video_output"] = response.choices[0].message.content

    if st.session_state["video_output"]:
        st.subheader("🎥 5 Short-Form Video Ideas")
        st.markdown(st.session_state["video_output"])

    st.divider()
    st.markdown("## 📄 Final Campaign Report")

    if st.button("📄 Generate Full CMO Campaign Report"):
        missing = []
        if not st.session_state["strategy_output"]:
            missing.append("Campaign Strategy")
        if not st.session_state["content_output"]:
            missing.append("21-Day Content Calendar")
        if not st.session_state["lead_output"]:
            missing.append("Lead Magnets")
        if not st.session_state["ads_output"]:
            missing.append("Paid Ads")
        if not st.session_state["video_output"]:
            missing.append("Video Ideas")

        if missing:
            st.warning(f"Generate these sections first: {', '.join(missing)}")
        else:
            with st.spinner("Assembling premium campaign report..."):
                combined = f"""
Campaign Inputs:
Business: {business}
Offer: {offer}
Audience: {audience}
Goal: {goal}
Platforms: {platforms}
Tone: {tone}
Emotional Trigger: {emotion}
CTA: {cta}
Budget: {budget}
Visual Style: {visual}
Notes: {notes}

Campaign Strategy:
{st.session_state["strategy_output"]}

21-Day Content Calendar:
{st.session_state["content_output"]}

Lead Magnet Ideas:
{st.session_state["lead_output"]}

Paid Ads:
{st.session_state["ads_output"]}

Video Ideas:
{st.session_state["video_output"]}
"""

                prompt = f"""
Act as Rain Intelligence in executive CMO reporting mode.

Turn the following campaign assets into one polished, premium, client-ready campaign report.

Keep all generated assets intact. Do not remove the 21 days, 10 ads, or 5 videos.

Format the final report as:

1. Executive Campaign Overview
2. Strategic Campaign Logic
3. Audience Psychology
4. Campaign Message System
5. 21-Day Content Calendar
6. Lead Magnet System
7. Paid Ad System
8. Video Content System
9. Visual Direction Guide
10. Posting and Launch Recommendations
11. KPI Suggestions
12. Final CMO Recommendation

Campaign Assets:
{combined}
"""

                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are Rain Intelligence, an executive CMO creating a premium campaign report."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.65,
                )
                st.session_state["full_report_output"] = response.choices[0].message.content

                try:
                    save_data("Campaign_Engine", {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "User_Role": st.session_state.get("user_role", "guest"),
                        "Business": business,
                        "Offer": offer,
                        "Audience": audience,
                        "Goal": goal,
                        "Platforms": platforms,
                        "Tone": tone,
                        "Emotional_Trigger": emotion,
                        "CTA": cta,
                        "Budget": budget,
                        "Visual_Style": visual,
                        "Notes": notes,
                        "Campaign_Strategy": st.session_state["strategy_output"],
                        "Content_21_Days": st.session_state["content_output"],
                        "Lead_Magnets": st.session_state["lead_output"],
                        "Paid_Ads": st.session_state["ads_output"],
                        "Video_Ideas": st.session_state["video_output"],
                        "Full_Report": st.session_state["full_report_output"],
                    })
                except Exception as save_error:
                    st.warning(f"Report generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Full CMO campaign report generated.")

    if st.session_state["full_report_output"]:
        st.subheader("📄 Full CMO Campaign Report")
        st.markdown(st.session_state["full_report_output"])

        pdf_buffer = create_pdf_buffer("Campaign Engine V3 Report", st.session_state["full_report_output"])

        st.download_button(
            "📄 Download Full Campaign Report",
            pdf_buffer,
            file_name="Campaign_Engine_V3_Report.pdf"
        )


if __name__ == "__main__":
    run()