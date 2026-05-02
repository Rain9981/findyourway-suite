import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


AI_MODEL = "gpt-4o"


def build_offer_prompt(
    business_name,
    industry,
    current_services,
    skills,
    target_audience,
    customer_pain_points,
    revenue_goal,
    delivery_capacity,
    price_position,
    innovation_direction,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in offer innovation and service monetization mode.

You are a high-level CMO, business model strategist, offer architect, service designer, and monetization consultant.

Create modern, profitable, practical service and offer ideas that fit the business.

Return the response in this exact structure:

1. Business Offer Snapshot
2. Current Revenue Opportunity
3. Service Gap Analysis
4. 10 New Service Ideas
   For each include:
   - Service Name
   - Description
   - Target Buyer
   - Why It Could Sell
   - Suggested Price Range
5. 5 Premium Package Ideas
   For each include:
   - Package Name
   - What Is Included
   - Best Buyer
   - Premium Angle
   - Suggested Price Range
6. 5 Add-On / Upsell Ideas
7. 5 Course, Workshop, or Digital Download Ideas
8. Recurring Revenue Ideas
9. Best First Offer to Launch
10. Offer Ladder Recommendation
11. Risks to Avoid
12. FYW Tool Match
13. Final Monetization Insight

Business Name:
{business_name}

Industry:
{industry}

Current Services:
{current_services}

Skills / Capabilities:
{skills}

Target Audience:
{target_audience}

Customer Pain Points:
{customer_pain_points}

Revenue Goal:
{revenue_goal}

Delivery Capacity:
{delivery_capacity}

Price Position:
{price_position}

Innovation Direction:
{innovation_direction}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Business Genius Engine
- Business Development
- Brand Positioning
- AI CMO Engine
- Strategic Simulator
- Marketing Hub
- Lead Generation
- Forecasting
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

    st.title("💡 Offer Innovation Engine")
    st.caption("Create new services, premium packages, add-ons, courses, downloads, and monetization ideas.")

    st.sidebar.header("💡 Offer Innovation Guide")
    st.sidebar.markdown("""
**What this tool does:**
- creates new service ideas
- builds premium packages
- suggests add-ons and upsells
- creates digital product/course ideas
- builds an offer ladder

**Best use:**
Use after Business Genius Engine, Business Development, or AI CMO Engine when you need new ways to increase revenue.

**Pro Tip:** The best new offer usually comes from combining what you already do well with a pain your audience already pays to solve.
""")

    defaults = {
        "oi_business_name": "",
        "oi_industry": "",
        "oi_current_services": "",
        "oi_skills": "",
        "oi_target_audience": "",
        "oi_customer_pain_points": "",
        "oi_revenue_goal": "",
        "oi_delivery_capacity": "Solo / limited capacity",
        "oi_price_position": "Mid-range",
        "oi_innovation_direction": "Premium service packages",
        "oi_optional_notes": "",
        "offer_innovation_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["oi_business_name"] = "Better N Clean"
        st.session_state["oi_industry"] = "Residential and Commercial Cleaning"
        st.session_state["oi_current_services"] = "Standard residential cleaning, deep cleaning, move-in/move-out cleaning, and commercial cleaning."
        st.session_state["oi_skills"] = "Cleaning operations, client service, quality control, property care, scheduling, team coordination, and local service delivery."
        st.session_state["oi_target_audience"] = "Busy homeowners, landlords, property managers, small offices, churches, and local businesses."
        st.session_state["oi_customer_pain_points"] = "Lack of time, inconsistent cleaners, unreliable service, messy move-outs, poor first impressions, and need for trustworthy recurring help."
        st.session_state["oi_revenue_goal"] = "Increase monthly recurring revenue and create higher-value service packages."
        st.session_state["oi_delivery_capacity"] = "Small team / moderate capacity"
        st.session_state["oi_price_position"] = "Mid-range"
        st.session_state["oi_innovation_direction"] = "Premium service packages"
        st.session_state["oi_optional_notes"] = "Ideas should be realistic for a local cleaning business but modern enough to stand out."

    st.markdown("### 📥 Offer Innovation Inputs")

    business_name = st.text_input("Business Name", key="oi_business_name")
    industry = st.text_input("Industry / Niche", key="oi_industry")

    current_services = st.text_area("Current Services", key="oi_current_services", height=100)
    skills = st.text_area("Skills / Capabilities", key="oi_skills", height=100)
    target_audience = st.text_area("Target Audience", key="oi_target_audience", height=100)
    customer_pain_points = st.text_area("Customer Pain Points", key="oi_customer_pain_points", height=100)
    revenue_goal = st.text_area("Revenue Goal", key="oi_revenue_goal", height=90)

    col1, col2, col3 = st.columns(3)

    with col1:
        delivery_capacity = st.selectbox(
            "Delivery Capacity",
            [
                "Solo / limited capacity",
                "Small team / moderate capacity",
                "Growing team",
                "Established operation",
                "Scalable digital delivery"
            ],
            key="oi_delivery_capacity"
        )

    with col2:
        price_position = st.selectbox(
            "Price Position",
            [
                "Budget-friendly",
                "Mid-range",
                "Premium",
                "Luxury / high-ticket",
                "Not sure"
            ],
            key="oi_price_position"
        )

    with col3:
        innovation_direction = st.selectbox(
            "Innovation Direction",
            [
                "Premium service packages",
                "Add-ons and upsells",
                "Digital products / downloads",
                "Courses or workshops",
                "Recurring subscription model",
                "Corporate / B2B offers",
                "All of the above"
            ],
            key="oi_innovation_direction"
        )

    optional_notes = st.text_area("Optional Notes", key="oi_optional_notes", height=100)

    if st.button("🚀 Generate Offer Ideas"):
        required = [
            business_name.strip(),
            industry.strip(),
            current_services.strip(),
            skills.strip(),
            target_audience.strip(),
            customer_pain_points.strip(),
            revenue_goal.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main offer innovation fields before generating.")
        else:
            try:
                with st.spinner("Generating offer innovation strategy..."):
                    prompt = build_offer_prompt(
                        business_name=business_name,
                        industry=industry,
                        current_services=current_services,
                        skills=skills,
                        target_audience=target_audience,
                        customer_pain_points=customer_pain_points,
                        revenue_goal=revenue_goal,
                        delivery_capacity=delivery_capacity,
                        price_position=price_position,
                        innovation_direction=innovation_direction,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model=AI_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in offer innovation mode: commercially sharp, creative, "
                                    "practical, premium-minded, and focused on revenue expansion."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.85,
                    )

                    output = response.choices[0].message.content
                    st.session_state["offer_innovation_result"] = output

                    try:
                        save_data("Offer_Innovation_Engine", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Business_Name": business_name,
                            "Industry": industry,
                            "Current_Services": current_services,
                            "Skills": skills,
                            "Target_Audience": target_audience,
                            "Customer_Pain_Points": customer_pain_points,
                            "Revenue_Goal": revenue_goal,
                            "Delivery_Capacity": delivery_capacity,
                            "Price_Position": price_position,
                            "Innovation_Direction": innovation_direction,
                            "Optional_Notes": optional_notes,
                            "Offer_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Offer innovation strategy generated.")
                st.subheader("💡 Offer Innovation Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("offer_innovation_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Offer Innovation Engine Report", st.session_state["offer_innovation_result"])

        st.download_button(
            "📄 Download Offer Innovation Report",
            pdf_buffer,
            file_name="Offer_Innovation_Engine_Report.pdf"
        )


if __name__ == "__main__":
    run()