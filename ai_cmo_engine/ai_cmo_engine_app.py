import streamlit as st
import datetime
import io
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from backend.email_utils import send_email
from backend.google_sheets import save_data


def build_cmo_prompt(
    business_name,
    business_stage,
    industry,
    revenue_range,
    primary_goal,
    current_marketing,
    current_challenges,
    target_audience,
    current_offers,
    visibility_status,
    lead_flow_status,
    conversion_status,
    team_capacity,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in its executive business strategy form: clear, structured, commercially aware, highly strategic, and practically useful.

You are not a generic marketing coach.
You are an elite Chief Marketing Officer-level business advisor focused on growth, visibility, lead generation, positioning, conversion, and execution.

Your job:
- analyze the business clearly
- identify the main bottlenecks slowing growth
- diagnose marketing, visibility, lead flow, and conversion issues
- identify realistic opportunities
- recommend exact next moves
- give a clear short-term execution path
- recommend exact FYW tools, tabs, or systems if they fit
- explain when upgrading within FYW InterNetwork could help this business
- if an outside recommendation is needed, say so honestly

Tone requirements:
- professional
- strategic
- commercially intelligent
- clear
- polished
- decisive
- not fluffy
- not overly emotional
- not vague

The output should feel like a premium strategic growth briefing from a real CMO.

Return the response in this exact structure:

1. Business Snapshot
2. Core Problems & Bottlenecks
3. Visibility and Market Position Read
4. Lead Generation Analysis
5. Conversion and Sales Read
6. Key Opportunities
7. Strategic Direction
8. Weekly Execution Plan
9. Next Best Actions
10. FYW Tool and Program Match
11. InterNetwork Upgrade Reason
12. External Strategic Recommendations
13. Final CMO Insight

Business Inputs:

Business Name:
{business_name}

Business Stage:
{business_stage}

Industry:
{industry}

Revenue Range:
{revenue_range}

Primary Goal:
{primary_goal}

Current Marketing Efforts:
{current_marketing}

Current Challenges:
{current_challenges}

Target Audience:
{target_audience}

Current Offers / Services:
{current_offers}

Current Visibility Status:
{visibility_status}

Current Lead Flow Status:
{lead_flow_status}

Current Conversion Status:
{conversion_status}

Current Team / Capacity:
{team_capacity}

Optional Additional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools / ecosystem to use when appropriate:
- Consulting Guide
- Brand Positioning
- Business Development
- Strategy Designer
- Business Model Canvas
- Business Genius Engine
- Lead Generation
- Marketing Hub
- Marketing Planner
- Email Marketing
- Sentiment Analysis
- Mastermind Analyzer
- Operations Audit
- Oops Audit
- Growth
- KPI Tracker
- Forecasting
- Canvas
- CRM
- CRM Dashboard
- Legacy Architecture
- FYW InterNetwork membership pathway

Important:
- In section 10, recommend exact FYW tools, tabs, systems, or programs if they clearly fit.
- In section 11, explain why moving upward through InterNetwork could help this business specifically.
- In section 12, include honest outside recommendations if needed such as CRM setup, website improvements, ad testing, sales training, legal setup, operations systems, or outside specialists.
- Make the output feel premium, practical, and directly tied to the business inputs.
"""


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🧠 AI CMO Engine")
    st.caption("A premium growth command tool built to analyze business position, identify bottlenecks, and deliver a clear strategic direction like a Chief Marketing Officer.")

    st.sidebar.header("📈 AI CMO Walkthrough")
    st.sidebar.markdown("""
**What this tool does:**
- reviews the business situation strategically
- identifies growth bottlenecks
- analyzes visibility, lead flow, and conversion issues
- recommends practical next moves
- gives a short-term execution path
- recommends FYW tools, systems, and InterNetwork pathways where relevant

**Instructions:**
1. Click **✨ Suggest CMO Example** if you want a sample.
2. Complete the main business and marketing fields honestly.
3. Add optional notes if relevant.
4. Click **🚀 Generate CMO Strategy**.
5. Download or email the output if needed.

**Pro Tip:** Clear inputs create sharper strategy. The more specific the business reality, the more valuable the output.
""")

    if st.button("✨ Suggest CMO Example"):
        st.session_state["cmo_autofill"] = {
            "business_name": "Better N Clean",
            "business_stage": "Growing",
            "industry": "Cleaning Services",
            "revenue_range": "$1K-$5K/month",
            "primary_goal": "Generate more consistent monthly clients and secure more commercial contracts.",
            "current_marketing": "Word of mouth, occasional Facebook posting, and some direct outreach. No real campaign structure, no consistent content system, and no strong follow-up process.",
            "current_challenges": "Inconsistent leads, low visibility, weak follow-up, unclear positioning, and no strong system for converting interest into recurring clients.",
            "target_audience": "Residential homeowners, property managers, small businesses, and commercial spaces needing reliable cleaning support.",
            "current_offers": "Residential cleaning, commercial cleaning, property clean-outs, and maintenance-related cleaning services.",
            "visibility_status": "Low visibility",
            "lead_flow_status": "Inconsistent leads",
            "conversion_status": "Some interest but few closes",
            "team_capacity": "Me with limited support",
            "optional_notes": "The business has strong service potential but needs more structure, stronger local visibility, and a more repeatable growth system."
        }

    def autofill_value(field, default=""):
        return st.session_state.get("cmo_autofill", {}).get(field, default)

    st.markdown("### 📥 AI CMO Input")

    business_name = st.text_input(
        "Business Name",
        value=autofill_value("business_name"),
        placeholder="Example: Better N Clean"
    )

    col1, col2 = st.columns(2)

    stage_options = [
        "Idea Stage",
        "Startup",
        "Early Growth",
        "Growing",
        "Established",
        "Scaling"
    ]

    revenue_options = [
        "No revenue yet",
        "Under $1K/month",
        "$1K-$5K/month",
        "$5K-$20K/month",
        "$20K-$50K/month",
        "$50K+/month"
    ]

    visibility_options = [
        "Almost no visibility",
        "Low visibility",
        "Some visibility but inconsistent",
        "Moderate visibility",
        "Strong visibility but weak conversion",
        "Strong visibility overall"
    ]

    lead_options = [
        "Almost no leads",
        "Inconsistent leads",
        "Some leads but not enough",
        "Steady leads but low quality",
        "Strong lead flow"
    ]

    conversion_options = [
        "Very weak conversion",
        "Some interest but few closes",
        "Moderate conversion",
        "Good conversion but low volume",
        "Strong conversion"
    ]

    team_options = [
        "Just me",
        "Me with limited support",
        "Small team",
        "Growing team",
        "Established team"
    ]

    with col1:
        business_stage = st.selectbox(
            "Business Stage",
            stage_options,
            index=stage_options.index(autofill_value("business_stage", "Startup")) if autofill_value("business_stage", "Startup") in stage_options else 1
        )

        industry = st.text_input(
            "Industry / Niche",
            value=autofill_value("industry"),
            placeholder="Example: Cleaning Services, Consulting, Real Estate, Retail"
        )

        revenue_range = st.selectbox(
            "Revenue Range",
            revenue_options,
            index=revenue_options.index(autofill_value("revenue_range", "No revenue yet")) if autofill_value("revenue_range", "No revenue yet") in revenue_options else 0
        )

        primary_goal = st.text_area(
            "Primary Goal",
            value=autofill_value("primary_goal"),
            height=100,
            placeholder="What is the main business result you want right now?"
        )

    with col2:
        visibility_status = st.selectbox(
            "Current Visibility Status",
            visibility_options,
            index=visibility_options.index(autofill_value("visibility_status", "Low visibility")) if autofill_value("visibility_status", "Low visibility") in visibility_options else 1
        )

        lead_flow_status = st.selectbox(
            "Current Lead Flow Status",
            lead_options,
            index=lead_options.index(autofill_value("lead_flow_status", "Inconsistent leads")) if autofill_value("lead_flow_status", "Inconsistent leads") in lead_options else 1
        )

        conversion_status = st.selectbox(
            "Current Conversion Status",
            conversion_options,
            index=conversion_options.index(autofill_value("conversion_status", "Some interest but few closes")) if autofill_value("conversion_status", "Some interest but few closes") in conversion_options else 1
        )

        team_capacity = st.selectbox(
            "Current Team / Capacity",
            team_options,
            index=team_options.index(autofill_value("team_capacity", "Just me")) if autofill_value("team_capacity", "Just me") in team_options else 0
        )

    current_marketing = st.text_area(
        "Current Marketing Efforts",
        value=autofill_value("current_marketing"),
        height=130,
        placeholder="What are you currently doing for marketing, promotion, content, referrals, outreach, ads, email, SEO, etc.?"
    )

    current_challenges = st.text_area(
        "Current Challenges",
        value=autofill_value("current_challenges"),
        height=130,
        placeholder="What is slowing growth right now? Be specific."
    )

    target_audience = st.text_area(
        "Target Audience",
        value=autofill_value("target_audience"),
        height=110,
        placeholder="Who are you trying to attract, serve, or convert?"
    )

    current_offers = st.text_area(
        "Current Offers / Services",
        value=autofill_value("current_offers"),
        height=110,
        placeholder="What are you selling right now?"
    )

    optional_notes = st.text_area(
        "Optional Additional Notes",
        value=autofill_value("optional_notes"),
        height=120,
        placeholder="Anything else that matters: market conditions, local competition, internal limitations, business goals, staffing, website issues, branding issues, etc."
    )

    email_enabled = st.checkbox("✅ Email me this CMO strategy")
    user_email = st.text_input("Enter your email:") if email_enabled else None

    if st.button("🚀 Generate CMO Strategy"):
        required_fields = [
            business_name.strip(),
            industry.strip(),
            primary_goal.strip(),
            current_marketing.strip(),
            current_challenges.strip(),
            target_audience.strip(),
            current_offers.strip(),
        ]

        if not all(required_fields):
            st.warning("⚠️ Please complete the main business fields before generating.")
        else:
            try:
                with st.spinner("Analyzing business position and generating CMO strategy..."):
                    prompt = build_cmo_prompt(
                        business_name=business_name,
                        business_stage=business_stage,
                        industry=industry,
                        revenue_range=revenue_range,
                        primary_goal=primary_goal,
                        current_marketing=current_marketing,
                        current_challenges=current_challenges,
                        target_audience=target_audience,
                        current_offers=current_offers,
                        visibility_status=visibility_status,
                        lead_flow_status=lead_flow_status,
                        conversion_status=conversion_status,
                        team_capacity=team_capacity,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in executive business strategy form: "
                                    "a high-level CMO advisor with strong strategic clarity, growth logic, "
                                    "commercial intelligence, and practical execution thinking."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["cmo_output"] = output

                    try:
                        save_data("AI_CMO_Engine", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Business_Name": business_name,
                            "Business_Stage": business_stage,
                            "Industry": industry,
                            "Revenue_Range": revenue_range,
                            "Primary_Goal": primary_goal,
                            "Current_Marketing": current_marketing,
                            "Current_Challenges": current_challenges,
                            "Target_Audience": target_audience,
                            "Current_Offers": current_offers,
                            "Visibility_Status": visibility_status,
                            "Lead_Flow_Status": lead_flow_status,
                            "Conversion_Status": conversion_status,
                            "Team_Capacity": team_capacity,
                            "Optional_Notes": optional_notes,
                            "Output": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Strategy generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ AI CMO strategy generated.")
                st.subheader("📈 Your CMO Strategy Briefing")
                st.markdown(output)

            except Exception as e:
                st.error(f"Error generating output: {e}")

    if "cmo_output" in st.session_state:
        output = st.session_state["cmo_output"]

        st.divider()

        role = st.session_state.get("user_role", "guest")
        st.markdown("### 🔓 Why This Tool Matters")

        if role == "basic":
            st.info(
                "This tool gives a strategic growth reading for the business. If the output reveals bigger needs around positioning, "
                "lead generation, execution systems, or visibility, higher InterNetwork levels can unlock stronger tools and support."
            )
        elif role == "elite":
            st.info(
                "You already have stronger strategic access. If your output reveals deeper needs around systems, campaigns, lead flow, "
                "or growth structure, the next level can help you move further."
            )
        elif role == "premium":
            st.info(
                "You already have expanded access. Use this strategy briefing to connect direction, execution, and growth optimization."
            )
        elif role == "admin":
            st.success(
                "This tool can help diagnose business bottlenecks and route clients into the right FYW tools, InterNetwork pathways, "
                "and strategic next steps."
            )

        st.markdown("### 🔗 Next Links")
        st.markdown("""
- [Upgrade Through FYW InterNetwork](https://findyourwaynmc.com/internetwork#internetwork-membership)
- [Visit FindYourWayNMC.com](https://findyourwaynmc.com)
- Use the **Consulting Guide** tab if you want help understanding the recommended tools next
""")

        pdf_buffer = io.BytesIO()
        pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, height - 40, "Your AI CMO Strategy Report")
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
            text.textLine(line)
            y_position -= 12

        pdf.drawText(text)
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button(
            "📄 Download AI CMO Strategy Report as PDF",
            data=pdf_buffer,
            file_name="AI_CMO_Strategy_Report.pdf"
        )

        if email_enabled and user_email:
            if st.button("📧 Send AI CMO Strategy to My Email"):
                try:
                    sent = send_email(
                        recipient_email=user_email,
                        subject="Your AI CMO Strategy Report",
                        body=output,
                        sender_email=st.secrets["email"]["smtp_user"],
                        sender_password=st.secrets["email"]["smtp_password"]
                    )
                    if sent:
                        st.success("📬 AI CMO strategy sent to your email!")
                    else:
                        st.error("❌ Failed to send email.")
                except Exception as e:
                    st.error(f"Email Error: {e}")


if __name__ == "__main__":
    run()