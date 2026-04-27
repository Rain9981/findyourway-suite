import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_lead_generation_prompt(
    audience,
    offer,
    lead_goal,
    current_channels,
    lead_magnet_type,
    funnel_stage,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in lead-generation strategy mode: conversion-focused, practical, strategic, and commercially clear.

You are helping the user create better lead magnets, outreach ideas, funnel entry points, and list-building strategy.

Return the response in this exact structure:

1. Lead Goal Snapshot
2. Ideal Lead Profile
3. Best Lead Magnet Ideas
4. Outreach Strategy
5. Funnel Entry Path
6. Conversion Angle
7. Follow-Up Sequence Idea
8. Risk or Weakness to Fix
9. FYW Tool Match
10. Next Best Actions
11. Final Lead Generation Insight

Target Audience:
{audience}

Offer / Service:
{offer}

Lead Goal:
{lead_goal}

Current Channels:
{current_channels}

Preferred Lead Magnet Type:
{lead_magnet_type}

Funnel Stage:
{funnel_stage}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Marketing Hub
- Email Marketing
- AI CMO Engine
- Strategic Simulator
- Network Builder
- Brand Positioning
- Business Development
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

    st.title("🎯 Lead Generation")
    st.caption("Create lead magnet ideas, outreach strategy, and funnel entry paths that attract the right audience.")

    st.sidebar.header("💡 Lead Generation Guide")
    st.sidebar.markdown("""
**What this tool does:**
- helps clarify who you are trying to attract
- creates lead magnet ideas
- builds outreach and funnel entry strategies
- improves list-building and conversion direction

**Pro Tip:** Lead generation works best when the audience, offer, and follow-up system are clearly connected.
""")

    defaults = {
        "lead_audience": "",
        "lead_offer": "",
        "lead_goal": "",
        "lead_channels": "",
        "lead_optional_notes": "",
        "lead_magnet_type": "Checklist / Guide",
        "lead_funnel_stage": "Top of Funnel",
        "lead_gen_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["lead_audience"] = (
            "Small business owners, entrepreneurs, and service providers who need stronger business structure, visibility, and marketing direction."
        )
        st.session_state["lead_offer"] = (
            "Find Your Way consulting tools, strategy guidance, AI-powered business support, and growth planning resources."
        )
        st.session_state["lead_goal"] = (
            "Collect qualified leads who are interested in improving their business and eventually upgrading into Elite or Premium access."
        )
        st.session_state["lead_channels"] = (
            "Website, social media posts, email outreach, QR code flyers, local networking, and InterNetwork referrals."
        )
        st.session_state["lead_magnet_type"] = "Checklist / Guide"
        st.session_state["lead_funnel_stage"] = "Top of Funnel"
        st.session_state["lead_optional_notes"] = (
            "The lead magnet should feel valuable, professional, and easy for busy business owners to understand quickly."
        )

    st.markdown("### 📥 Lead Generation Input")

    audience = st.text_area(
        "Target Audience",
        key="lead_audience",
        height=100,
        placeholder="Who are you trying to attract?"
    )

    offer = st.text_area(
        "Offer / Service",
        key="lead_offer",
        height=100,
        placeholder="What are you offering or promoting?"
    )

    col1, col2 = st.columns(2)

    with col1:
        lead_magnet_type = st.selectbox(
            "Preferred Lead Magnet Type",
            [
                "Checklist / Guide",
                "Mini Workbook",
                "Assessment / Quiz",
                "Free Consultation",
                "Template",
                "Webinar / Training",
                "Discount / Offer",
                "Resource Vault"
            ],
            key="lead_magnet_type"
        )

    with col2:
        funnel_stage = st.selectbox(
            "Funnel Stage",
            [
                "Top of Funnel",
                "Middle of Funnel",
                "Bottom of Funnel",
                "Reactivation",
                "Referral Funnel"
            ],
            key="lead_funnel_stage"
        )

    lead_goal = st.text_area(
        "Lead Goal",
        key="lead_goal",
        height=100,
        placeholder="Example: collect emails, book calls, attract local clients, build a list, qualify prospects, etc."
    )

    current_channels = st.text_area(
        "Current Channels",
        key="lead_channels",
        height=100,
        placeholder="Example: website, social media, email, ads, referrals, QR flyers, events, etc."
    )

    optional_notes = st.text_area(
        "Optional Notes",
        key="lead_optional_notes",
        height=100,
        placeholder="Add any context about budget, launch timing, current audience size, or conversion issues."
    )

    if st.button("🚀 Generate Lead Strategy"):
        required = [
            audience.strip(),
            offer.strip(),
            lead_goal.strip(),
            current_channels.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main lead generation fields before generating.")
        else:
            try:
                with st.spinner("Generating lead strategy..."):
                    prompt = build_lead_generation_prompt(
                        audience=audience,
                        offer=offer,
                        lead_goal=lead_goal,
                        current_channels=current_channels,
                        lead_magnet_type=lead_magnet_type,
                        funnel_stage=funnel_stage,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in lead-generation strategy mode: conversion-focused, "
                                    "practical, clear, and focused on attracting qualified prospects."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["lead_gen_result"] = output

                    try:
                        save_data("Lead_Generation", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Target_Audience": audience,
                            "Offer": offer,
                            "Lead_Goal": lead_goal,
                            "Current_Channels": current_channels,
                            "Lead_Magnet_Type": lead_magnet_type,
                            "Funnel_Stage": funnel_stage,
                            "Optional_Notes": optional_notes,
                            "Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Strategy generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Lead strategy generated.")
                st.subheader("🎯 Lead Generation Strategy")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    if st.session_state.get("lead_gen_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Lead Generation Report", st.session_state["lead_gen_result"])

        st.download_button(
            "📄 Download Lead Generation Report",
            data=pdf_buffer,
            file_name="Lead_Generation_Report.pdf"
        )


if __name__ == "__main__":
    run()