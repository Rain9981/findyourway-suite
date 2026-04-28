import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_marketing_hub_prompt(product_service, audience, campaign_goal, brand_message, offer_angle, channels, tone, optional_notes):
    return f"""
Act as Rain Intelligence in marketing strategy mode: persuasive, clear, audience-aware, and brand-focused.

Return this exact structure:

1. Campaign Snapshot
2. Audience Psychology
3. Core Message Angle
4. Offer Positioning
5. Content Themes
6. Channel Strategy
7. Hook Ideas
8. Messaging Risks to Avoid
9. FYW Tool Match
10. Next Best Actions
11. Final Marketing Insight

Product / Service:
{product_service}

Target Audience:
{audience}

Campaign Goal:
{campaign_goal}

Current Brand Message:
{brand_message}

Offer Angle:
{offer_angle}

Marketing Channels:
{channels}

Tone:
{tone}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Brand Positioning
- Lead Generation
- Email Marketing
- Sentiment Analysis
- AI CMO Engine
- Marketing Planner
- Strategic Simulator
"""


def create_pdf_buffer(title, output):
    buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 40, title)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")

    text = pdf.beginText(50, height - 90)
    text.setFont("Helvetica", 10)
    y = height - 90

    for line in output.split("\n"):
        if y < 50:
            pdf.drawText(text)
            pdf.showPage()
            text = pdf.beginText(50, height - 50)
            text.setFont("Helvetica", 10)
            y = height - 50
        text.textLine(line[:110])
        y -= 12

    pdf.drawText(text)
    pdf.save()
    buffer.seek(0)
    return buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("📣 Marketing Hub")
    st.caption("Shape your campaign message, content angle, audience psychology, and brand direction.")

    st.sidebar.header("💡 Marketing Hub Guide")
    st.sidebar.markdown("""
**What this tool does:**
- refines campaign ideas
- sharpens brand messaging
- creates content themes and hooks
- helps position an offer before planning execution

**Best use:**
Use before Marketing Planner, Email Marketing, or Lead Generation.

**Pro Tip:** The Hub helps you decide what the campaign should say before you decide exactly when and where to publish it.
""")

    defaults = {
        "mh_product_service": "",
        "mh_audience": "",
        "mh_campaign_goal": "",
        "mh_brand_message": "",
        "mh_offer_angle": "",
        "mh_channels": "",
        "mh_optional_notes": "",
        "mh_tone": "Professional / Persuasive",
        "marketing_hub_result": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.button("✨ Autofill Example"):
        st.session_state["mh_product_service"] = "Find Your Way Elite Access"
        st.session_state["mh_audience"] = "Small business owners and entrepreneurs who need structure, clarity, and growth tools."
        st.session_state["mh_campaign_goal"] = "Promote Elite access and show why it is the best starting point for serious builders."
        st.session_state["mh_brand_message"] = "Find Your Way helps people move from scattered ideas to structured growth."
        st.session_state["mh_offer_angle"] = "Unlock strategy, AI tools, and execution guidance without guessing what to do next."
        st.session_state["mh_channels"] = "Website, email, social media, InterNetwork page, and direct outreach."
        st.session_state["mh_tone"] = "Professional / Persuasive"
        st.session_state["mh_optional_notes"] = "Campaign should feel premium, clear, and action-driven."

    st.markdown("### 📥 Marketing Hub Input")

    product_service = st.text_area("Product / Service", key="mh_product_service", height=90)
    audience = st.text_area("Target Audience", key="mh_audience", height=90)
    campaign_goal = st.text_area("Campaign Goal", key="mh_campaign_goal", height=90)
    brand_message = st.text_area("Current Brand Message", key="mh_brand_message", height=90)
    offer_angle = st.text_area("Offer Angle", key="mh_offer_angle", height=90)
    channels = st.text_area("Marketing Channels", key="mh_channels", height=90)

    tone = st.selectbox(
        "Tone",
        [
            "Professional / Persuasive",
            "Warm / Relatable",
            "Luxury / Premium",
            "Bold / Direct",
            "Educational / Helpful",
            "Visionary / Inspirational"
        ],
        key="mh_tone"
    )

    optional_notes = st.text_area("Optional Notes", key="mh_optional_notes", height=90)

    if st.button("🚀 Generate Marketing Strategy"):
        required = [product_service.strip(), audience.strip(), campaign_goal.strip(), offer_angle.strip()]
        if not all(required):
            st.warning("⚠️ Please complete the main marketing fields before generating.")
        else:
            try:
                with st.spinner("Generating marketing strategy..."):
                    prompt = build_marketing_hub_prompt(
                        product_service, audience, campaign_goal, brand_message,
                        offer_angle, channels, tone, optional_notes
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are Rain Intelligence in marketing strategy mode: clear, persuasive, audience-aware, and brand-focused."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["marketing_hub_result"] = output

                    try:
                        save_data("Marketing_Hub", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Product_Service": product_service,
                            "Audience": audience,
                            "Campaign_Goal": campaign_goal,
                            "Brand_Message": brand_message,
                            "Offer_Angle": offer_angle,
                            "Channels": channels,
                            "Tone": tone,
                            "Optional_Notes": optional_notes,
                            "Marketing_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Marketing strategy generated.")
                st.subheader("📣 Marketing Hub Strategy")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("marketing_hub_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Marketing Hub Strategy Report", st.session_state["marketing_hub_result"])
        st.download_button("📄 Download Marketing Hub Report", pdf_buffer, file_name="Marketing_Hub_Report.pdf")


if __name__ == "__main__":
    run()