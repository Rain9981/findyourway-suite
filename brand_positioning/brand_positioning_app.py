import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_brand_positioning_prompt(
    brand_name,
    industry,
    target_audience,
    brand_promise,
    differentiator,
    competitors,
    brand_personality,
    desired_perception,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in premium brand strategy mode: clear, sharp, psychologically aware, and market-position focused.

You are helping define a strong brand position that clarifies who the brand serves, what makes it different, why it matters, and how it should be perceived.

Return the response in this exact structure:

1. Brand Snapshot
2. Ideal Audience Read
3. Core Differentiator
4. Market Positioning Statement
5. Brand Promise
6. Emotional Value Proposition
7. Competitive Separation
8. Messaging Pillars
9. Brand Voice Direction
10. FYW Tool Match
11. Next Best Actions
12. Final Brand Insight

Brand Name:
{brand_name}

Industry:
{industry}

Target Audience:
{target_audience}

Brand Promise:
{brand_promise}

Main Differentiator:
{differentiator}

Competitors / Alternatives:
{competitors}

Brand Personality:
{brand_personality}

Desired Market Perception:
{desired_perception}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Business Genius Engine
- Strategy Designer
- Marketing Hub
- Sentiment Analysis
- AI CMO Engine
- Lead Generation
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

    st.title("🏷️ Brand Positioning")
    st.caption("Clarify your market position, brand promise, audience, and differentiation strategy.")

    st.sidebar.header("💡 Brand Positioning Guide")
    st.sidebar.markdown("""
**What this tool does:**
- clarifies who your brand is for
- defines what makes your brand different
- strengthens brand promise and perception
- creates positioning language you can use in marketing

**Pro Tip:** Strong positioning makes marketing easier because people understand who you are, what you do, and why you matter.
""")

    defaults = {
        "brand_name": "",
        "brand_industry": "",
        "brand_target_audience": "",
        "brand_promise": "",
        "brand_differentiator": "",
        "brand_competitors": "",
        "brand_optional_notes": "",
        "brand_personality": "Premium / Professional",
        "brand_desired_perception": "Trusted and high-value",
        "brand_positioning_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Example"):
        st.session_state["brand_name"] = "Find Your Way Network Marketing Consultants"
        st.session_state["brand_industry"] = "Business Consulting, AI Strategy, and Growth Systems"
        st.session_state["brand_target_audience"] = (
            "Small business owners, entrepreneurs, creators, and service providers who need strategy, structure, visibility, and growth direction."
        )
        st.session_state["brand_promise"] = (
            "We help people move from confusion to structure by giving them strategic tools, AI-powered guidance, and clear execution pathways."
        )
        st.session_state["brand_differentiator"] = (
            "Unlike basic consulting or generic business advice, Find Your Way combines AI tools, CMO-level strategy, personal development, and a connected growth ecosystem."
        )
        st.session_state["brand_competitors"] = (
            "Traditional consultants, online business coaches, marketing agencies, and generic AI tools."
        )
        st.session_state["brand_personality"] = "Premium / Professional"
        st.session_state["brand_desired_perception"] = "Trusted and high-value"
        st.session_state["brand_optional_notes"] = (
            "The brand should feel intelligent, structured, empowering, and premium without being confusing."
        )

    st.markdown("### 📥 Brand Positioning Input")

    brand_name = st.text_input(
        "Brand Name",
        key="brand_name",
        placeholder="Example: Find Your Way Network Marketing Consultants"
    )

    industry = st.text_input(
        "Industry / Niche",
        key="brand_industry",
        placeholder="Example: Consulting, wellness, cleaning, design, finance, education"
    )

    target_audience = st.text_area(
        "Target Audience",
        key="brand_target_audience",
        height=100,
        placeholder="Who is this brand designed to serve?"
    )

    brand_promise = st.text_area(
        "Brand Promise",
        key="brand_promise",
        height=100,
        placeholder="What transformation, result, or value does the brand promise?"
    )

    differentiator = st.text_area(
        "Main Differentiator",
        key="brand_differentiator",
        height=100,
        placeholder="What makes this brand different from competitors or alternatives?"
    )

    competitors = st.text_area(
        "Competitors / Alternatives",
        key="brand_competitors",
        height=90,
        placeholder="Who else does the audience compare you to?"
    )

    col1, col2 = st.columns(2)

    with col1:
        brand_personality = st.selectbox(
            "Brand Personality",
            [
                "Premium / Professional",
                "Bold / Disruptive",
                "Warm / Relatable",
                "Luxury / Elegant",
                "Educational / Trusted",
                "Innovative / Futuristic",
                "Community-Focused",
                "Spiritual / Purpose-Driven"
            ],
            key="brand_personality"
        )

    with col2:
        desired_perception = st.selectbox(
            "Desired Market Perception",
            [
                "Trusted and high-value",
                "Exclusive and premium",
                "Helpful and accessible",
                "Innovative and advanced",
                "Community-centered",
                "Results-driven",
                "Luxury and refined",
                "Transformational"
            ],
            key="brand_desired_perception"
        )

    optional_notes = st.text_area(
        "Optional Notes",
        key="brand_optional_notes",
        height=100,
        placeholder="Add any tone, market, story, pricing, design, or audience details."
    )

    if st.button("🚀 Generate Brand Positioning"):
        required = [
            brand_name.strip(),
            industry.strip(),
            target_audience.strip(),
            brand_promise.strip(),
            differentiator.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main brand fields before generating.")
        else:
            try:
                with st.spinner("Generating brand positioning strategy..."):
                    prompt = build_brand_positioning_prompt(
                        brand_name=brand_name,
                        industry=industry,
                        target_audience=target_audience,
                        brand_promise=brand_promise,
                        differentiator=differentiator,
                        competitors=competitors,
                        brand_personality=brand_personality,
                        desired_perception=desired_perception,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in brand positioning mode: premium, clear, strategic, "
                                    "psychologically aware, and focused on market differentiation."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["brand_positioning_result"] = output

                    try:
                        save_data("Brand_Positioning", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Brand_Name": brand_name,
                            "Industry": industry,
                            "Target_Audience": target_audience,
                            "Brand_Promise": brand_promise,
                            "Differentiator": differentiator,
                            "Competitors": competitors,
                            "Brand_Personality": brand_personality,
                            "Desired_Perception": desired_perception,
                            "Optional_Notes": optional_notes,
                            "Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Positioning generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Brand positioning generated.")
                st.subheader("🏷️ Brand Positioning Strategy")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    if st.session_state.get("brand_positioning_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Brand Positioning Report", st.session_state["brand_positioning_result"])

        st.download_button(
            "📄 Download Brand Positioning Report",
            data=pdf_buffer,
            file_name="Brand_Positioning_Report.pdf"
        )


if __name__ == "__main__":
    run()