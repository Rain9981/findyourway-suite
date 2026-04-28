import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_canvas_prompt(
    business_name,
    business_stage,
    industry,
    value_proposition,
    customer_segments,
    customer_problem,
    revenue_streams,
    channels,
    customer_relationships,
    key_activities,
    key_resources,
    key_partners,
    cost_structure,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in business model architecture mode: strategic, structured, commercially sharp, and execution-focused.

You are helping build a premium Business Model Canvas that explains how the business creates, delivers, and captures value.

Return the response in this exact structure:

1. Business Snapshot
2. Value Proposition
3. Customer Segments
4. Customer Problem Being Solved
5. Channels
6. Customer Relationships
7. Revenue Streams
8. Key Activities
9. Key Resources
10. Key Partners
11. Cost Structure
12. Strategic Strengths
13. Weak Points / Gaps
14. FYW Tool Match
15. Next Best Actions
16. Final Business Model Insight

Business Name:
{business_name}

Business Stage:
{business_stage}

Industry:
{industry}

Value Proposition:
{value_proposition}

Customer Segments:
{customer_segments}

Customer Problem:
{customer_problem}

Revenue Streams:
{revenue_streams}

Channels:
{channels}

Customer Relationships:
{customer_relationships}

Key Activities:
{key_activities}

Key Resources:
{key_resources}

Key Partners:
{key_partners}

Cost Structure:
{cost_structure}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Business Genius Engine
- Brand Positioning
- Strategy Designer
- AI CMO Engine
- Strategic Simulator
- Lead Generation
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

    st.title("🧩 Business Model Canvas")
    st.caption("Build a structured business model that clarifies how your business creates, delivers, and captures value.")

    st.sidebar.header("💡 Business Model Canvas Guide")
    st.sidebar.markdown("""
**What this tool does:**
- builds a strategic business model canvas
- clarifies the offer, audience, channels, costs, and revenue
- identifies gaps in the business model
- connects the model to the next FYW tools

**What to enter:**
- Business idea or name
- Target customers
- Problem being solved
- Revenue streams
- Key activities, partners, and resources

**Best use:**
Use this after the Business Genius Engine or before Strategy Designer when you need to organize the business model clearly.

**Pro Tip:** A strong business model is not just a good idea. It must show how value is created, delivered, paid for, and sustained.
""")

    defaults = {
        "bmc_business_name": "",
        "bmc_industry": "",
        "bmc_value_proposition": "",
        "bmc_customer_segments": "",
        "bmc_customer_problem": "",
        "bmc_revenue_streams": "",
        "bmc_channels": "",
        "bmc_customer_relationships": "",
        "bmc_key_activities": "",
        "bmc_key_resources": "",
        "bmc_key_partners": "",
        "bmc_cost_structure": "",
        "bmc_optional_notes": "",
        "bmc_business_stage": "Startup",
        "canvas_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["bmc_business_name"] = "Mobile Auto Detail Pro"
        st.session_state["bmc_business_stage"] = "Startup"
        st.session_state["bmc_industry"] = "Mobile Car Detailing"
        st.session_state["bmc_value_proposition"] = (
            "Premium car detailing delivered directly to busy professionals at their home or workplace."
        )
        st.session_state["bmc_customer_segments"] = (
            "Busy professionals, urban residents, luxury car owners, rideshare drivers, and small business fleet owners."
        )
        st.session_state["bmc_customer_problem"] = (
            "Customers want clean, well-maintained vehicles but do not have time to wait at a shop or handle detailing themselves."
        )
        st.session_state["bmc_revenue_streams"] = (
            "One-time detailing services, monthly maintenance packages, fleet service contracts, add-on upsells, and premium detailing bundles."
        )
        st.session_state["bmc_channels"] = (
            "Website, Google Business Profile, social media, local partnerships, referral program, QR flyers, and direct outreach."
        )
        st.session_state["bmc_customer_relationships"] = (
            "Easy booking, follow-up reminders, loyalty discounts, recurring maintenance plans, and personalized service."
        )
        st.session_state["bmc_key_activities"] = (
            "Detailing services, appointment scheduling, customer follow-up, local marketing, supply management, and quality control."
        )
        st.session_state["bmc_key_resources"] = (
            "Detailing equipment, trained staff, transportation, booking system, customer list, brand assets, and cleaning supplies."
        )
        st.session_state["bmc_key_partners"] = (
            "Auto shops, apartment buildings, property managers, dealerships, local businesses, and supply vendors."
        )
        st.session_state["bmc_cost_structure"] = (
            "Labor, supplies, transportation, equipment, insurance, marketing, software, and maintenance costs."
        )
        st.session_state["bmc_optional_notes"] = (
            "The business wants to position itself as convenient, premium, and reliable."
        )

    st.markdown("### 📥 Business Model Canvas Input")

    business_name = st.text_input(
        "Business Name",
        key="bmc_business_name",
        placeholder="Example: Mobile Auto Detail Pro"
    )

    col1, col2 = st.columns(2)

    with col1:
        business_stage = st.selectbox(
            "Business Stage",
            ["Idea Stage", "Startup", "Growing", "Established", "Scaling"],
            key="bmc_business_stage"
        )

    with col2:
        industry = st.text_input(
            "Industry / Niche",
            key="bmc_industry",
            placeholder="Example: Cleaning, consulting, design, wellness, auto services"
        )

    value_proposition = st.text_area(
        "Value Proposition",
        key="bmc_value_proposition",
        height=100,
        placeholder="What value does this business deliver?"
    )

    customer_segments = st.text_area(
        "Customer Segments",
        key="bmc_customer_segments",
        height=100,
        placeholder="Who are the main customer groups?"
    )

    customer_problem = st.text_area(
        "Customer Problem Being Solved",
        key="bmc_customer_problem",
        height=100,
        placeholder="What problem, pain point, or desire does this business address?"
    )

    col3, col4 = st.columns(2)

    with col3:
        revenue_streams = st.text_area(
            "Revenue Streams",
            key="bmc_revenue_streams",
            height=120,
            placeholder="How will the business make money?"
        )

        channels = st.text_area(
            "Channels",
            key="bmc_channels",
            height=120,
            placeholder="How will customers discover, access, or buy from the business?"
        )

        key_activities = st.text_area(
            "Key Activities",
            key="bmc_key_activities",
            height=120,
            placeholder="What must the business do consistently to operate?"
        )

    with col4:
        customer_relationships = st.text_area(
            "Customer Relationships",
            key="bmc_customer_relationships",
            height=120,
            placeholder="How will the business attract, serve, retain, and follow up with customers?"
        )

        key_resources = st.text_area(
            "Key Resources",
            key="bmc_key_resources",
            height=120,
            placeholder="What assets, people, tools, or systems are required?"
        )

        key_partners = st.text_area(
            "Key Partners",
            key="bmc_key_partners",
            height=120,
            placeholder="Who could support, supply, refer, or strengthen the model?"
        )

    cost_structure = st.text_area(
        "Cost Structure",
        key="bmc_cost_structure",
        height=100,
        placeholder="What costs must be managed?"
    )

    optional_notes = st.text_area(
        "Optional Notes",
        key="bmc_optional_notes",
        height=100,
        placeholder="Add anything else about pricing, positioning, audience, operations, or competition."
    )

    if st.button("🚀 Generate Business Model Canvas"):
        required = [
            business_name.strip(),
            industry.strip(),
            value_proposition.strip(),
            customer_segments.strip(),
            customer_problem.strip(),
            revenue_streams.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main business model fields before generating.")
        else:
            try:
                with st.spinner("Building your business model canvas..."):
                    prompt = build_canvas_prompt(
                        business_name=business_name,
                        business_stage=business_stage,
                        industry=industry,
                        value_proposition=value_proposition,
                        customer_segments=customer_segments,
                        customer_problem=customer_problem,
                        revenue_streams=revenue_streams,
                        channels=channels,
                        customer_relationships=customer_relationships,
                        key_activities=key_activities,
                        key_resources=key_resources,
                        key_partners=key_partners,
                        cost_structure=cost_structure,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in business model architecture mode: structured, strategic, "
                                    "commercially sharp, and focused on turning ideas into viable business models."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.75,
                    )

                    output = response.choices[0].message.content
                    st.session_state["canvas_result"] = output

                    try:
                        save_data("Business_Model_Canvas", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Business_Name": business_name,
                            "Business_Stage": business_stage,
                            "Industry": industry,
                            "Value_Proposition": value_proposition,
                            "Customer_Segments": customer_segments,
                            "Customer_Problem": customer_problem,
                            "Revenue_Streams": revenue_streams,
                            "Channels": channels,
                            "Customer_Relationships": customer_relationships,
                            "Key_Activities": key_activities,
                            "Key_Resources": key_resources,
                            "Key_Partners": key_partners,
                            "Cost_Structure": cost_structure,
                            "Optional_Notes": optional_notes,
                            "Canvas_Output": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Canvas generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Business Model Canvas generated.")
                st.subheader("🧩 Business Model Canvas Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("canvas_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Business Model Canvas Report", st.session_state["canvas_result"])

        st.download_button(
            "📄 Download Business Model Canvas Report",
            data=pdf_buffer,
            file_name="Business_Model_Canvas_Report.pdf"
        )


if __name__ == "__main__":
    run()