import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_business_development_prompt(
    business_name,
    growth_goal,
    current_position,
    opportunity_type,
    target_market,
    potential_partners,
    current_resources,
    main_challenge,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in business development strategy mode: commercially sharp, strategic, practical, and growth-focused.

You are helping identify partnership, expansion, revenue, and growth opportunities.

Return the response in this exact structure:

1. Business Development Snapshot
2. Growth Opportunity Read
3. Best Partnership or Expansion Targets
4. Strategic Fit Analysis
5. Revenue Potential
6. Main Risks or Friction Points
7. Recommended Growth Path
8. Outreach or Activation Strategy
9. FYW Tool Match
10. Next Best Actions
11. Final Business Development Insight

Business Name:
{business_name}

Growth Goal:
{growth_goal}

Current Position:
{current_position}

Opportunity Type:
{opportunity_type}

Target Market:
{target_market}

Potential Partners:
{potential_partners}

Current Resources:
{current_resources}

Main Challenge:
{main_challenge}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- AI CMO Engine
- Strategic Simulator
- Network Builder
- Lead Generation
- Marketing Hub
- Strategy Designer
- Forecasting
- KPI Tracker
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

    st.title("🏗️ Business Development")
    st.caption("Identify growth opportunities, partnership pathways, expansion moves, and revenue-building strategies.")

    st.sidebar.header("💡 Business Development Guide")
    st.sidebar.markdown("""
**What this tool does:**
- identifies growth and expansion opportunities
- helps structure partnership ideas
- clarifies revenue and market development paths
- connects business development to execution strategy

**Pro Tip:** Business development is not just “getting bigger” — it is choosing the right opportunities, partners, and growth paths with strategic fit.
""")

    defaults = {
        "biz_dev_business_name": "",
        "biz_dev_growth_goal": "",
        "biz_dev_current_position": "",
        "biz_dev_target_market": "",
        "biz_dev_potential_partners": "",
        "biz_dev_current_resources": "",
        "biz_dev_main_challenge": "",
        "biz_dev_optional_notes": "",
        "biz_dev_opportunity_type": "Strategic Partnerships",
        "business_dev_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["biz_dev_business_name"] = "Find Your Way Network Marketing Consultants"
        st.session_state["biz_dev_growth_goal"] = (
            "Expand the ecosystem by building stronger partnerships, increasing visibility, "
            "and creating more pathways for business owners to enter the FYW system."
        )
        st.session_state["biz_dev_current_position"] = (
            "The business has consulting services, AI tools, an InterNetwork direction, and multiple growth programs, "
            "but needs clearer partnership pathways and structured expansion moves."
        )
        st.session_state["biz_dev_opportunity_type"] = "Strategic Partnerships"
        st.session_state["biz_dev_target_market"] = (
            "Small business owners, entrepreneurs, service providers, local businesses, coaches, consultants, and creators."
        )
        st.session_state["biz_dev_potential_partners"] = (
            "Marketing professionals, local business associations, financial educators, coaches, real estate professionals, "
            "design agencies, and service-based businesses."
        )
        st.session_state["biz_dev_current_resources"] = (
            "Website, consulting suite, AI tools, InterNetwork concept, strategy frameworks, course content, and lead funnels."
        )
        st.session_state["biz_dev_main_challenge"] = (
            "The main challenge is organizing opportunities into a clear growth path without spreading the brand too thin."
        )
        st.session_state["biz_dev_optional_notes"] = (
            "The growth strategy should protect the premium feel of the brand while still making collaboration easier."
        )

    st.markdown("### 📥 Business Development Input")

    business_name = st.text_input(
        "Business Name",
        key="biz_dev_business_name",
        placeholder="Example: Find Your Way Network Marketing Consultants"
    )

    growth_goal = st.text_area(
        "Growth Goal",
        key="biz_dev_growth_goal",
        height=110,
        placeholder="What are you trying to grow, expand, launch, or develop?"
    )

    current_position = st.text_area(
        "Current Business Position",
        key="biz_dev_current_position",
        height=110,
        placeholder="Where is the business now? What exists already?"
    )

    col1, col2 = st.columns(2)

    with col1:
        opportunity_type = st.selectbox(
            "Opportunity Type",
            [
                "Strategic Partnerships",
                "New Market Expansion",
                "New Service / Offer",
                "Referral Growth",
                "Affiliate Development",
                "Community / Network Expansion",
                "Corporate / B2B Opportunity",
                "Local Business Development"
            ],
            key="biz_dev_opportunity_type"
        )

    with col2:
        main_challenge = st.text_area(
            "Main Challenge",
            key="biz_dev_main_challenge",
            height=120,
            placeholder="What is the biggest issue slowing this growth opportunity?"
        )

    target_market = st.text_area(
        "Target Market",
        key="biz_dev_target_market",
        height=100,
        placeholder="Who is this opportunity meant to reach?"
    )

    potential_partners = st.text_area(
        "Potential Partners or Channels",
        key="biz_dev_potential_partners",
        height=100,
        placeholder="Who or what could help this grow? Partners, platforms, groups, companies, communities, etc."
    )

    current_resources = st.text_area(
        "Current Resources / Assets",
        key="biz_dev_current_resources",
        height=100,
        placeholder="What do you already have that can support this opportunity?"
    )

    optional_notes = st.text_area(
        "Optional Notes",
        key="biz_dev_optional_notes",
        height=100,
        placeholder="Add context about timing, budget, market, staffing, audience, or brand direction."
    )

    if st.button("🚀 Generate Business Development Strategy"):
        required = [
            business_name.strip(),
            growth_goal.strip(),
            current_position.strip(),
            target_market.strip(),
            main_challenge.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main business development fields before generating.")
        else:
            try:
                with st.spinner("Generating business development strategy..."):
                    prompt = build_business_development_prompt(
                        business_name=business_name,
                        growth_goal=growth_goal,
                        current_position=current_position,
                        opportunity_type=opportunity_type,
                        target_market=target_market,
                        potential_partners=potential_partners,
                        current_resources=current_resources,
                        main_challenge=main_challenge,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in business development mode: strategic, commercially sharp, "
                                    "growth-focused, partnership-aware, and practical."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["business_dev_result"] = output

                    try:
                        save_data("Business_Development", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Business_Name": business_name,
                            "Growth_Goal": growth_goal,
                            "Current_Position": current_position,
                            "Opportunity_Type": opportunity_type,
                            "Target_Market": target_market,
                            "Potential_Partners": potential_partners,
                            "Current_Resources": current_resources,
                            "Main_Challenge": main_challenge,
                            "Optional_Notes": optional_notes,
                            "Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Strategy generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Business development strategy generated.")
                st.subheader("🏗️ Business Development Strategy")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    if st.session_state.get("business_dev_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Business Development Report", st.session_state["business_dev_result"])

        st.download_button(
            "📄 Download Business Development Report",
            data=pdf_buffer,
            file_name="Business_Development_Report.pdf"
        )


if __name__ == "__main__":
    run()