import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


AI_MODEL = "gpt-4o"


BURGUNDY = colors.HexColor("#800020")
GOLD = colors.HexColor("#D4AF37")
BLACK = colors.HexColor("#111111")
LIGHT_GOLD = colors.HexColor("#F6E8B1")


def add_page_header_footer(canvas, doc):
    canvas.saveState()

    canvas.setStrokeColor(BURGUNDY)
    canvas.setLineWidth(1)
    canvas.line(50, 760, 562, 760)

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(BURGUNDY)
    canvas.drawString(50, 772, "Find Your Way Network Marketing Consultants")

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(562, 30, f"Page {doc.page}")

    canvas.restoreState()


def create_business_plan_pdf(title, output, business_name="", goal="", stage=""):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=BURGUNDY,
        alignment=1,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        textColor=BLACK,
        alignment=1,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=BURGUNDY,
        spaceBefore=14,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="BodyClean",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=BLACK,
        spaceAfter=7
    ))

    styles.add(ParagraphStyle(
        name="SmallGold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=GOLD,
        alignment=1
    ))

    story = []

    # Cover Page
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("Professional Business Plan", styles["CoverTitle"]))

    if business_name:
        story.append(Paragraph(business_name, styles["CoverSubtitle"]))

    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Prepared by Find Your Way Network Marketing Consultants", styles["SmallGold"]))
    story.append(Paragraph("Powered by Rain Intelligence", styles["SmallGold"]))

    story.append(Spacer(1, 0.5 * inch))

    cover_data = [
        ["Primary Goal", goal if goal else "Not specified"],
        ["Business Stage", stage if stage else "Not specified"],
        ["Generated", datetime.date.today().strftime("%B %d, %Y")]
    ]

    cover_table = Table(cover_data, colWidths=[1.8 * inch, 4.2 * inch])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BURGUNDY),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),
        ("TEXTCOLOR", (1, 0), (1, -1), BLACK),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    story.append(cover_table)

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        "This document is designed as a structured planning, presentation, and decision-support asset. "
        "It should be reviewed, customized, and refined before being shared with investors, partners, lenders, or stakeholders.",
        styles["CoverSubtitle"]
    ))

    story.append(PageBreak())

    # Body content
    for raw_line in output.split("\n"):
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        clean_line = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        is_heading = False

        section_starts = [
            "1.", "2.", "3.", "4.", "5.", "6.", "7.",
            "8.", "9.", "10.", "11.", "12.", "13.", "14.",
            "Executive Summary",
            "Problem & Opportunity",
            "Solution / Offering",
            "Market Analysis",
            "Business Model",
            "Competitive Positioning",
            "Brand & Vision Alignment",
            "Marketing Strategy",
            "Operations Plan",
            "Growth Strategy",
            "Financial Direction",
            "Funding / Investment Angle",
            "Team & Role Structure",
            "Next Action Plan",
            "Final Business Plan Note"
        ]

        if any(clean_line.startswith(start) for start in section_starts):
            is_heading = True

        if is_heading and len(clean_line) < 120:
            story.append(Paragraph(clean_line, styles["SectionHeading"]))
        else:
            story.append(Paragraph(clean_line, styles["BodyClean"]))

    doc.build(
        story,
        onFirstPage=add_page_header_footer,
        onLaterPages=add_page_header_footer
    )

    buffer.seek(0)
    return buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("📘 Business Plan Generator")
    st.caption("Generate a complete professional business plan for launch, growth, funding, or internal clarity.")

    st.sidebar.header("📘 Business Plan Guide")
    st.sidebar.markdown("""
**What this tool does:**
- Creates a finished business plan document
- Structures the idea into investor-ready sections
- Adapts the plan based on launch, funding, growth, or clarity
- Helps users produce a usable document, not just strategy notes

**This is not:**
- Business Model Canvas
- Strategy Designer
- Business Development
- General brainstorming

**Best use:**
Use after the client already has a business idea, offer, audience, or direction and needs a professional compiled plan.
""")

    defaults = {
        "bpg_idea": "",
        "bpg_audience": "",
        "bpg_problem": "",
        "bpg_offer": "",
        "bpg_revenue": "",
        "bpg_stage": "Idea",
        "bpg_goal": "Launch",
        "bpg_team": "",
        "bpg_location": "",
        "bpg_budget": "",
        "bpg_output": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["bpg_idea"] = "A premium AI-powered consulting platform that helps small business owners organize branding, marketing, strategy, growth, and client management in one guided system."
        st.session_state["bpg_audience"] = "Small business owners, entrepreneurs, consultants, service providers, and creators who need structure, strategy, and execution support."
        st.session_state["bpg_problem"] = "Many business owners have ideas, services, and customers, but lack a clear plan, organized execution system, and professional strategy document."
        st.session_state["bpg_offer"] = "A tier-based AI consulting suite with tools for brand clarity, campaign planning, lead generation, business development, CRM support, forecasting, and strategic decision-making."
        st.session_state["bpg_revenue"] = "Monthly subscriptions, premium consulting packages, downloadable business tools, course bundles, and done-with-you strategy sessions."
        st.session_state["bpg_stage"] = "Startup"
        st.session_state["bpg_goal"] = "Growth"
        st.session_state["bpg_team"] = "Founder-led with future contractors, consultants, designers, marketers, and automation support."
        st.session_state["bpg_location"] = "Online platform with local consulting expansion."
        st.session_state["bpg_budget"] = "Lean startup budget with phased reinvestment into automation, marketing, and platform upgrades."

    st.markdown("### 📥 Business Plan Inputs")

    idea = st.text_area("Business Idea or Concept", key="bpg_idea", height=110)
    audience = st.text_area("Target Audience", key="bpg_audience", height=90)
    problem = st.text_area("Problem Being Solved", key="bpg_problem", height=90)
    offer = st.text_area("Product or Service", key="bpg_offer", height=100)
    revenue = st.text_area("Revenue Model", key="bpg_revenue", height=90)

    col1, col2 = st.columns(2)

    with col1:
        stage = st.selectbox(
            "Business Stage",
            ["Idea", "Startup", "Scaling"],
            key="bpg_stage"
        )

        team = st.text_area("Optional: Team Size / Team Notes", key="bpg_team", height=80)

    with col2:
        goal = st.selectbox(
            "Primary Goal",
            ["Launch", "Funding", "Growth", "Internal Clarity"],
            key="bpg_goal"
        )

        location = st.text_input("Optional: Location / Market Area", key="bpg_location")

    budget = st.text_input("Optional: Budget / Financial Context", key="bpg_budget")

    required = idea.strip() and audience.strip() and problem.strip() and offer.strip() and revenue.strip()

    st.divider()

    if st.button("📘 Generate Complete Business Plan"):
        if not required:
            st.warning("Please complete Business Idea, Audience, Problem, Product/Service, and Revenue Model first.")
        else:
            with st.spinner("Building your complete business plan..."):
                prompt = f"""
Act as Rain Intelligence inside the Find Your Way AI Consulting Suite.

You are running the Business Plan Generator.

Purpose:
Generate a complete, structured, professional business plan based on user inputs.

Important boundaries:
- This is NOT a strategy suggestion tool.
- This is NOT Business Model Canvas.
- This is NOT Strategy Designer.
- This is NOT Business Development.
- Do not output loose bullet suggestions.
- Output a finished, ready-to-use business plan document.
- The document should be usable for planning, presentations, internal direction, or investors.

Adaptation Rules:
- If Primary Goal is Funding, make the plan more investor-focused.
- If Primary Goal is Launch, make the plan more execution-focused.
- If Primary Goal is Growth, make the plan more scaling-focused.
- If Primary Goal is Internal Clarity, make the plan more organizational and direction-focused.

Tone:
Professional, structured, polished, and investor-ready when needed.

User Inputs:
Business Idea or Concept: {idea}
Target Audience: {audience}
Problem Being Solved: {problem}
Product or Service: {offer}
Revenue Model: {revenue}
Business Stage: {stage}
Primary Goal: {goal}
Team Size / Team Notes: {team}
Location / Market Area: {location}
Budget / Financial Context: {budget}

Create a complete business plan with these exact sections:

1. Executive Summary
Write this like a real executive summary, not a list.

2. Problem & Opportunity
Explain the problem, the opportunity, and why now matters.

3. Solution / Offering
Describe the product or service as a clear business solution.

4. Market Analysis
Explain the target market, customer need, demand logic, and market potential based on the user's input. Do not invent fake statistics.

5. Business Model
Explain how the business makes money, who pays, and what drives repeat revenue.

6. Competitive Positioning
Explain how the business can stand apart from alternatives or competitors.

7. Brand & Vision Alignment
Explain the deeper brand direction, customer promise, and long-term identity.

8. Marketing Strategy
Create a practical marketing strategy connected to the goal.

9. Operations Plan
Explain how the business should function day to day.

10. Growth Strategy
Explain how the business can expand, scale, or strengthen over time.

11. Financial Direction
Explain financial priorities, budget logic, revenue focus, and cost awareness. Do not create fake projections unless clearly framed as example ranges.

12. Funding / Investment Angle
Only include this section if the selected goal is Funding. If not funding, write: "Not applicable to this plan based on the selected goal."

13. Team & Role Structure
Include current and future role recommendations. If team information is limited, explain the minimum role structure needed.

14. Next Action Plan
Give a clear action plan with immediate next steps.

End with:
Final Business Plan Note
A polished closing paragraph that explains how the user should use this document.
"""

                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Rain Intelligence, an executive business planning strategist creating polished business plan documents."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.65,
                )

                st.session_state["bpg_output"] = response.choices[0].message.content

                try:
                    save_data("Business_Plan_Generator", {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "User_Role": st.session_state.get("user_role", "guest"),
                        "Business_Idea": idea,
                        "Target_Audience": audience,
                        "Problem": problem,
                        "Product_Service": offer,
                        "Revenue_Model": revenue,
                        "Business_Stage": stage,
                        "Primary_Goal": goal,
                        "Team": team,
                        "Location": location,
                        "Budget": budget,
                        "AI_Output": st.session_state["bpg_output"],
                    })
                    st.success("✅ Business Plan generated and saved.")
                except Exception as save_error:
                    st.warning(f"Business plan generated, but Google Sheets save had an issue: {save_error}")

    if st.session_state["bpg_output"]:
        st.subheader("✅ Complete Business Plan")
        st.markdown(st.session_state["bpg_output"])

        pdf_buffer = create_business_plan_pdf(
            "Business Plan Generator Report",
            st.session_state["bpg_output"],
            business_name=st.session_state.get("bpg_idea", ""),
            goal=st.session_state.get("bpg_goal", ""),
            stage=st.session_state.get("bpg_stage", "")
        )

        st.download_button(
            "📄 Download Investor-Style Business Plan PDF",
            pdf_buffer,
            file_name="Business_Plan_Generator_Investor_Style_Report.pdf",
            mime="application/pdf"
        )


if __name__ == "__main__":
    run()