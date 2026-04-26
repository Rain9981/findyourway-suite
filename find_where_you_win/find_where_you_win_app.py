import streamlit as st
import datetime
import io
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from backend.email_utils import send_email
from backend.google_sheets import save_data


def build_find_where_you_win_prompt(
    city,
    state,
    zip_area,
    nearby_areas,
    service_mode,
    goal_vision,
    problem_to_solve,
    target_audience,
    desired_outcome,
    current_position,
    current_assets,
    skills_resources,
    natural_strengths,
    oversaturated,
    missing,
    complaints,
    underserved,
    opportunity_preferences,
    weekly_time,
    startup_budget,
    risk_level,
    income_goal,
    vision_plan,
    network_plan,
    notes,
):
    return f"""
Act as Rain Intelligence™ operating as a high-level Market Intelligence Engine, CMO strategist, business architect, opportunity analyst, and local economic strategist for Find Your Way Network Marketing Consultants.

You are not a generic business idea generator.
You are diagnosing where this person has the highest probability of winning based on location, market awareness, skills, resources, risk level, and goals.

You must think like:
- a local market analyst
- a Chief Marketing Officer
- a business strategist
- a demographic opportunity mapper
- an execution planner
- a wealth pathway advisor

Important:
- Do not claim to have live data unless live data is provided.
- If live data is not provided, use informed market reasoning, demographic assumptions, urban/suburban business patterns, consumer behavior patterns, and strategic inference.
- Do not sound generic.
- Do not repeat the user's answers back.
- Interpret the data and produce a premium consulting-style report.
- Be decisive, practical, and commercially intelligent.

USER INPUTS:

Location:
City: {city}
State: {state}
Zip / Neighborhood: {zip_area}
Nearby Service Areas: {nearby_areas}
Service Mode: {service_mode}

Goal / Vision:
{goal_vision}

Problem They Want to Solve:
{problem_to_solve}

Audience They Want to Help:
{target_audience}

Desired Customer Outcome:
{desired_outcome}

Current Position:
{current_position}

Current Assets:
{current_assets}

Skills / Resources:
{skills_resources}

Natural Strengths:
{natural_strengths}

Market Awareness:
Oversaturated Market Observations:
{oversaturated}

Missing Opportunities:
{missing}

Common Complaints:
{complaints}

Underserved Groups:
{underserved}

Opportunity Preferences:
{opportunity_preferences}

Capacity:
Weekly Time Available:
{weekly_time}

Startup Budget:
{startup_budget}

Risk Level:
{risk_level}

Income Goal:
{income_goal}

Optional Vision Builder Plan:
{vision_plan if vision_plan.strip() else "None provided"}

Optional Network Builder Plan:
{network_plan if network_plan.strip() else "None provided"}

Optional Notes:
{notes if notes.strip() else "None provided"}

Return the response in this exact structure:

# FIND WHERE YOU WIN™ MARKET INTELLIGENCE REPORT

## 1. Executive Strategic Snapshot
Give a sharp summary of the user's strongest opportunity direction.
Explain what kind of opportunity profile they appear to have.

## 2. Local Market Intelligence Snapshot
Analyze the likely market environment based on the city, state, neighborhood, and surrounding areas.

Include:
- likely customer behavior
- business density assumptions
- local service demand patterns
- online vs local opportunity fit
- possible economic and demographic patterns

Do not pretend to have exact live data unless provided.

## 3. Demand vs Saturation Analysis

### Oversaturated or Difficult Areas
Identify what may be too crowded, hard to enter, or weak for this person right now.

### Underserved or Weakly Served Areas
Identify what may be missing, poorly executed, or overlooked.

### Hidden Opportunity
Identify the opportunity most people overlook.

## 4. Demographic Opportunity Map
Identify likely customer groups worth targeting.

Include:
- age / life-stage groups
- income or lifestyle patterns
- household types
- business owner types
- community groups
- underserved customer segments

Explain why each demographic matters.

## 5. Skill-to-Market Alignment
Match the user's skills, resources, and natural strengths to practical opportunities.

Include:
- best immediate fit
- best scalable fit
- best long-term wealth fit
- what they should avoid based on their current position

## 6. Top 5 Opportunity Plays
Rank 5 opportunities from strongest to weakest.

For each opportunity include:
- Opportunity name
- Why it fits this person
- Why it fits this location / market
- Target customer
- Startup difficulty: Low / Medium / High
- Startup requirements
- Income potential: Low / Moderate / Strong / High
- Time to traction
- First move to test it

## 7. Gap Analysis

### Market Gap
What the area or audience appears to be missing.

### Positioning Gap
How competitors or similar providers may be failing to stand out.

### Execution Gap
What the user must build, learn, or organize to win.

### Resource Gap
What tools, people, funding, or systems are missing.

### Trust Gap
What proof, credibility, or authority must be built.

## 8. Positioning Advantage Blueprint
Create a clear positioning strategy.

Include:
- recommended market position
- brand angle
- message angle
- proof strategy
- what makes them different
- how to enter the market without looking like everyone else

## 9. Revenue Pathways

### Quick Cash Opportunities: 0–30 Days
Fast income plays they can test quickly.

### Growth Income Opportunities: 30–90 Days
Offers, services, or systems they can build.

### Long-Term Wealth Plays: 90 Days and Beyond
Scalable, investment, ownership, licensing, digital, or recurring models.

## 10. Execution Roadmap

### First 7 Days
Immediate research, outreach, setup, or validation actions.

### First 30 Days
Testing, offer creation, local validation, digital setup.

### Days 31–60
Marketing, partnerships, first sales, proof building.

### Days 61–90
Refinement, scale, automation, stronger positioning.

## 11. What It Takes to Win
Tell the user the truth.

Include:
- required discipline
- required skill development
- likely obstacles
- what they must stop doing
- what they must focus on

## 12. FYW Tool and Program Match
Recommend exact Find Your Way tools, tabs, programs, or pathways if they clearly fit.

Use from:
- Consulting Guide
- Brand Positioning
- Business Development
- Strategy Designer
- Business Model Canvas
- Business Genius Engine
- Lead Generation
- Network Builder
- Marketing Hub
- Marketing Planner
- Email Marketing
- AI CMO Engine
- Strategic Simulator
- Sentiment Analysis
- Operations Audit
- Growth
- KPI Tracker
- Forecasting
- Future Self Deep State
- Credit Repair
- Legacy Architecture
- FYW InterNetwork membership pathway

## 13. Final Rain Intelligence Recommendation
Give a decisive strategic conclusion.

Answer:
- where they should focus first
- what opportunity has the strongest signal
- what they should not waste time on
- what their next best move is

End with a powerful but professional advisory tone.
"""


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🌍 Find Where You Win™ Engine")
    st.caption(
        "A premium market intelligence tool built to identify local opportunity gaps, income pathways, demographic targets, and strategic next moves."
    )

    st.sidebar.header("🌍 Market Intelligence Walkthrough")
    st.sidebar.markdown("""
**What this tool does:**
- analyzes your location, skills, goals, resources, and market awareness
- identifies local business gaps and income opportunities
- maps demographic opportunity areas
- ranks the strongest opportunity plays
- creates a 90-day execution roadmap
- recommends relevant FYW tools and next steps

**Instructions:**
1. Click **✨ Suggest Market Intelligence Example** if you want a sample.
2. Complete each section with as much detail as possible.
3. Add Vision Builder or Network Builder notes if you already have them.
4. Click **🚀 Run Find Where I Win™ Analysis**.
5. Download or email the report if needed.

**Pro Tip:** The stronger your inputs, the more precise the opportunity analysis becomes.
""")

    if st.button("✨ Suggest Market Intelligence Example"):
        st.session_state["fwyw_autofill"] = {
            "city": "Chicago",
            "state": "Illinois",
            "zip_area": "South Suburbs / Chicago area",
            "nearby_areas": "Dolton, South Holland, Calumet City, Harvey, Homewood, Lansing, and nearby Chicago neighborhoods",
            "service_mode": "Both local and online",
            "goal_vision": "I want to build a service-based business that can generate consistent income, grow into a trusted local brand, and eventually create scalable systems.",
            "problem_to_solve": "Many local homeowners, small businesses, and property owners need reliable, professional services but struggle to find trustworthy providers with strong communication and follow-up.",
            "target_audience": "Homeowners, property managers, small business owners, busy professionals, and local organizations.",
            "desired_outcome": "I want customers to feel supported, confident, and relieved because the service solves a real problem and is delivered professionally.",
            "current_position": "Have an idea but need structure",
            "current_assets": "Some business experience, local knowledge, phone, computer, social media access, basic network, and willingness to start lean.",
            "skills_resources": "Communication, creative thinking, customer service, business planning, design, marketing ideas, and ability to organize services.",
            "natural_strengths": "I am good at seeing opportunities, connecting ideas, understanding people, and creating systems around a vision.",
            "oversaturated": "Basic cleaning companies, food businesses, clothing brands, and general social media promotion.",
            "missing": "Professional service providers with strong branding, follow-up, customer experience, and package-based offers.",
            "complaints": "People complain about unreliable contractors, poor communication, inconsistent service, weak professionalism, and businesses not following up.",
            "underserved": "Elderly homeowners, busy working families, small businesses, landlords, property managers, and local entrepreneurs.",
            "opportunity_preferences": "Local service business, consulting / coaching, creative business, technology / AI, and community-based business",
            "weekly_time": "10–20 hours per week",
            "startup_budget": "$500–$1,500",
            "risk_level": "Moderate risk",
            "income_goal": "Both fast income and long-term wealth",
            "vision_plan": "",
            "network_plan": "",
            "notes": "I want the opportunity to be realistic but also expandable into something bigger."
        }

    def autofill_value(field, default=""):
        return st.session_state.get("fwyw_autofill", {}).get(field, default)

    st.markdown("### 📍 Section 1: Location Intelligence")
    st.info(
        "For best results, complete every major section. This engine uses your location, skills, market awareness, and resources to identify where you may have the strongest chance to win."
    )

    col1, col2 = st.columns(2)

    with col1:
        city = st.text_input("City", value=autofill_value("city"), placeholder="Example: Chicago")
        state = st.text_input("State", value=autofill_value("state"), placeholder="Example: Illinois")
        zip_area = st.text_input(
            "Zip Code / Neighborhood / Area",
            value=autofill_value("zip_area"),
            placeholder="Example: South Suburbs, 60619, Downtown, West Side"
        )

    with col2:
        nearby_areas = st.text_area(
            "Nearby cities or areas you are willing to serve",
            value=autofill_value("nearby_areas"),
            height=110,
            placeholder="List nearby towns, suburbs, neighborhoods, counties, or regions."
        )

        service_mode_options = [
            "Local only",
            "Online only",
            "Both local and online",
            "Nationwide",
            "Not sure yet"
        ]

        service_mode = st.selectbox(
            "Do you want to serve locally, online, or both?",
            service_mode_options,
            index=service_mode_options.index(autofill_value("service_mode", "Both local and online"))
            if autofill_value("service_mode", "Both local and online") in service_mode_options else 2
        )

    st.markdown("### 🧭 Section 2: Goal + Vision")

    goal_vision = st.text_area(
        "What are you trying to build, create, or achieve?",
        value=autofill_value("goal_vision"),
        height=130,
        placeholder="Describe the business, income path, service, investment direction, or opportunity you want to explore."
    )

    problem_to_solve = st.text_area(
        "What problem do you want to solve?",
        value=autofill_value("problem_to_solve"),
        height=110,
        placeholder="What pain, need, frustration, gap, or demand do you want to address?"
    )

    col3, col4 = st.columns(2)

    with col3:
        target_audience = st.text_area(
            "Who do you want to help?",
            value=autofill_value("target_audience"),
            height=120,
            placeholder="Example: homeowners, parents, entrepreneurs, seniors, local businesses, creators, etc."
        )

    with col4:
        desired_outcome = st.text_area(
            "What result do you want people to get?",
            value=autofill_value("desired_outcome"),
            height=120,
            placeholder="What change, relief, gain, improvement, or outcome should your customer experience?"
        )

    st.markdown("### 🧱 Section 3: Current Position")

    current_position_options = [
        "Just exploring",
        "Have an idea",
        "Already running a business",
        "Have customers",
        "Have income but need growth",
        "Looking for a new income path"
    ]

    current_position = st.selectbox(
        "Where are you starting from?",
        current_position_options,
        index=current_position_options.index(autofill_value("current_position", "Have an idea"))
        if autofill_value("current_position", "Have an idea") in current_position_options else 1
    )

    current_assets = st.text_area(
        "What do you already have in place?",
        value=autofill_value("current_assets"),
        height=120,
        placeholder="Examples: website, social media, product, service, team, equipment, space, funding, customer list, license, software, vehicle, etc."
    )

    st.markdown("### 🧠 Section 4: Skills + Resources")

    skills_resources = st.text_area(
        "What skills, experience, talents, or resources do you already have?",
        value=autofill_value("skills_resources"),
        height=130,
        placeholder="Include work experience, business experience, trade skills, creative skills, people skills, money, equipment, tools, software, contacts, etc."
    )

    natural_strengths = st.text_area(
        "What are you naturally good at that people ask you for help with?",
        value=autofill_value("natural_strengths"),
        height=110,
        placeholder="Example: organizing, designing, motivating, cleaning, fixing, planning, selling, teaching, connecting people, managing details, spotting problems."
    )

    st.markdown("### 🔎 Section 5: Market Awareness")

    col5, col6 = st.columns(2)

    with col5:
        oversaturated = st.text_area(
            "What do you see too much of in your city or market?",
            value=autofill_value("oversaturated"),
            height=130,
            placeholder="What businesses, offers, trends, or services feel crowded, copied, low quality, or oversaturated?"
        )

        complaints = st.text_area(
            "What do people around you complain about?",
            value=autofill_value("complaints"),
            height=130,
            placeholder="What frustrations do you hear from customers, family, coworkers, business owners, homeowners, parents, etc.?"
        )

    with col6:
        missing = st.text_area(
            "What do you think is missing?",
            value=autofill_value("missing"),
            height=130,
            placeholder="What services, products, support, professionalism, convenience, or experiences are missing in your area?"
        )

        underserved = st.text_area(
            "What customers, communities, or groups seem underserved?",
            value=autofill_value("underserved"),
            height=130,
            placeholder="Example: seniors, small business owners, working parents, youth, landlords, homeowners, creators, tradespeople, etc."
        )

    st.markdown("### 💼 Section 6: Opportunity Preference")

    opportunity_options = [
        "Local service business",
        "Online business",
        "Product-based business",
        "Real estate / property",
        "Investing",
        "Consulting / coaching",
        "Creative business",
        "Technology / AI",
        "Community-based business",
        "Not sure yet"
    ]

    opportunity_preferences = st.multiselect(
        "Which opportunity types interest you most?",
        opportunity_options,
        default=autofill_value("opportunity_preferences", "Local service business").split(", ")
        if autofill_value("opportunity_preferences") else ["Local service business"]
    )

    st.markdown("### ⚖️ Section 7: Capacity + Risk")

    col7, col8 = st.columns(2)

    with col7:
        weekly_time = st.text_input(
            "How much time can you commit weekly?",
            value=autofill_value("weekly_time"),
            placeholder="Example: 5 hours, 10–20 hours, full-time"
        )

        startup_budget = st.text_input(
            "How much money can you realistically invest to start?",
            value=autofill_value("startup_budget"),
            placeholder="Example: $0–$250, $500, $1,500, $5,000+"
        )

    with col8:
        risk_options = [
            "Low risk",
            "Moderate risk",
            "Aggressive / high reward"
        ]

        risk_level = st.selectbox(
            "What risk level fits you?",
            risk_options,
            index=risk_options.index(autofill_value("risk_level", "Moderate risk"))
            if autofill_value("risk_level", "Moderate risk") in risk_options else 1
        )

        income_options = [
            "Fast income",
            "Long-term wealth",
            "Both fast income and long-term wealth",
            "Not sure yet"
        ]

        income_goal = st.selectbox(
            "Do you want fast income, long-term wealth, or both?",
            income_options,
            index=income_options.index(autofill_value("income_goal", "Both fast income and long-term wealth"))
            if autofill_value("income_goal", "Both fast income and long-term wealth") in income_options else 2
        )

    st.markdown("### 🧩 Section 8: Optional Advanced Paste Fields")

    vision_plan = st.text_area(
        "Optional: Paste Vision Builder Plan",
        value=autofill_value("vision_plan"),
        height=130,
        placeholder="Paste your Vision Builder or 30-60-90 plan if you already have one."
    )

    network_plan = st.text_area(
        "Optional: Paste Network Builder Plan",
        value=autofill_value("network_plan"),
        height=130,
        placeholder="Paste your Network Builder plan, team structure, partnership notes, or role map if available."
    )

    notes = st.text_area(
        "Optional: Additional Notes",
        value=autofill_value("notes"),
        height=120,
        placeholder="Anything else that matters: business ideas, research, local conditions, personal constraints, goals, fears, opportunities, or resources."
    )

    email_enabled = st.checkbox("✅ Email me this Market Intelligence Report")
    user_email = st.text_input("Enter your email:") if email_enabled else None

    if st.button("🚀 Run Find Where I Win™ Analysis"):
        required_fields = [
            city.strip(),
            state.strip(),
            goal_vision.strip(),
            problem_to_solve.strip(),
            target_audience.strip(),
            desired_outcome.strip(),
            current_assets.strip(),
            skills_resources.strip(),
            natural_strengths.strip(),
            oversaturated.strip(),
            missing.strip(),
            complaints.strip(),
            underserved.strip(),
            weekly_time.strip(),
            startup_budget.strip(),
        ]

        if not all(required_fields):
            st.warning("⚠️ Please complete the main fields before running the analysis. The stronger your inputs, the stronger the intelligence report.")
        else:
            try:
                with st.spinner("Scanning your market signals, skills, gaps, and opportunity pathways..."):
                    prompt = build_find_where_you_win_prompt(
                        city=city,
                        state=state,
                        zip_area=zip_area,
                        nearby_areas=nearby_areas,
                        service_mode=service_mode,
                        goal_vision=goal_vision,
                        problem_to_solve=problem_to_solve,
                        target_audience=target_audience,
                        desired_outcome=desired_outcome,
                        current_position=current_position,
                        current_assets=current_assets,
                        skills_resources=skills_resources,
                        natural_strengths=natural_strengths,
                        oversaturated=oversaturated,
                        missing=missing,
                        complaints=complaints,
                        underserved=underserved,
                        opportunity_preferences=", ".join(opportunity_preferences),
                        weekly_time=weekly_time,
                        startup_budget=startup_budget,
                        risk_level=risk_level,
                        income_goal=income_goal,
                        vision_plan=vision_plan,
                        network_plan=network_plan,
                        notes=notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence™, an elite market intelligence strategist, "
                                    "CMO advisor, local opportunity analyst, and business architect. "
                                    "Your analysis must be precise, strategic, commercially useful, "
                                    "demographic-aware, and action-oriented."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.82,
                    )

                    output = response.choices[0].message.content
                    st.session_state["fwyw_output"] = output

                    try:
                        save_data("Find_Where_You_Win", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "City": city,
                            "State": state,
                            "Zip_Area": zip_area,
                            "Nearby_Areas": nearby_areas,
                            "Service_Mode": service_mode,
                            "Goal_Vision": goal_vision,
                            "Problem_To_Solve": problem_to_solve,
                            "Target_Audience": target_audience,
                            "Desired_Outcome": desired_outcome,
                            "Current_Position": current_position,
                            "Current_Assets": current_assets,
                            "Skills_Resources": skills_resources,
                            "Natural_Strengths": natural_strengths,
                            "Oversaturated": oversaturated,
                            "Missing": missing,
                            "Complaints": complaints,
                            "Underserved": underserved,
                            "Opportunity_Preferences": ", ".join(opportunity_preferences),
                            "Weekly_Time": weekly_time,
                            "Startup_Budget": startup_budget,
                            "Risk_Level": risk_level,
                            "Income_Goal": income_goal,
                            "Vision_Plan": vision_plan,
                            "Network_Plan": network_plan,
                            "Notes": notes,
                            "Output": output,
                        }, sheet_tab="Find_Where_You_Win")
                    except Exception as save_error:
                        st.warning(f"Report generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Find Where You Win™ analysis generated.")
                st.subheader("🌍 Your Market Intelligence Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"Error generating output: {e}")

    if "fwyw_output" in st.session_state:
        output = st.session_state["fwyw_output"]

        st.divider()

        role = st.session_state.get("user_role", "guest")
        st.markdown("### 🔓 Why This Tool Matters")

        if role == "basic":
            st.info(
                "This market intelligence report gives a strong opportunity read. Higher InterNetwork levels can unlock deeper tools, "
                "execution support, business systems, and strategy pathways."
            )
        elif role == "elite":
            st.info(
                "Use this report to choose your strongest opportunity path, then move into Brand Positioning, Business Development, "
                "Lead Generation, Network Builder, or AI CMO Engine for execution."
            )
        elif role == "premium":
            st.info(
                "Use this report as a strategic decision map. Pair it with Marketing Planner, Email Marketing, Forecasting, KPI Tracker, "
                "and CRM tools to turn the opportunity into a measurable growth system."
            )
        elif role == "admin":
            st.success(
                "Admin note: This tool can help identify client opportunity direction, market fit, positioning gaps, and routing into the right FYW programs."
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
        pdf.drawString(50, height - 40, "Find Where You Win Market Intelligence Report")
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

        st.download_button(
            "📄 Download Market Intelligence Report as PDF",
            data=pdf_buffer,
            file_name="Find_Where_You_Win_Market_Intelligence_Report.pdf"
        )

        if email_enabled and user_email:
            if st.button("📧 Send Market Intelligence Report to My Email"):
                try:
                    sent = send_email(
                        recipient_email=user_email,
                        subject="Your Find Where You Win Market Intelligence Report",
                        body=output,
                        sender_email=st.secrets["email"]["smtp_user"],
                        sender_password=st.secrets["email"]["smtp_password"]
                    )
                    if sent:
                        st.success("📬 Market Intelligence Report sent to your email!")
                    else:
                        st.error("❌ Failed to send email.")
                except Exception as e:
                    st.error(f"Email Error: {e}")


if __name__ == "__main__":
    run()