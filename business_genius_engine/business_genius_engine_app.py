import streamlit as st
import datetime
import json
import io
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from backend.email_utils import send_email


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    st.title("🧠 Business Genius Engine")
    st.caption("Your AI-powered strategic transformation engine.")

    # 🧠 Sidebar Consulting Guide
    st.sidebar.header("🧠 Genius Strategy Guide")
    st.sidebar.markdown("""
    **What this tool does:**
    - Generates a complete business growth strategy using GPT.
    - Includes tailored advice for branding, marketing, credit, and more.

    **Instructions:**
    1. Use the toggle to select your business stage.
    2. Click **🔮 Suggest Smart Defaults** for a sample scenario.
    3. Complete or revise the business info fields.
    4. Click **🚀 Generate My Genius Strategy** to run AI logic.
    5. Optionally download your plan or receive it by email.

    **Pro Tip:** The strategy adapts based on your inputs — be specific!
    """)


    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    # Autofill logic toggle
    col_toggle, col_button = st.columns([0.6, 0.4])
    with col_toggle:
        business_stage = st.radio("Select your business stage:", ["Just starting", "Already successful"])
    with col_button:
        if st.button("🔮 Suggest Smart Defaults"):
            if business_stage == "Just starting":
                st.session_state["autofill"] = {
                    "business_name": "GlowWell Skincare",
                    "business_type": "We provide plant-based skincare for women age 30+ with sensitive skin.",
                    "audience": "Health-conscious women aged 30–50",
                    "goal": "Build initial audience and drive traffic",
                    "budget": 500,
                    "market_scope": "Online",
                    "stage": "Just starting",
                    "visibility_source": "Instagram, word of mouth",
                    "differentiator": "Clean, herbal formulas with subscription option",
                    "focus_area": "Marketing"
                }
            else:
                st.session_state["autofill"] = {
                    "business_name": "Elevate Financial Coaching",
                    "business_type": "1-on-1 financial coaching for entrepreneurs and couples",
                    "audience": "Entrepreneurs age 30–55 with inconsistent income",
                    "goal": "Attract high-paying clients and launch a premium offer",
                    "budget": 2500,
                    "market_scope": "Nationwide",
                    "stage": "Already successful",
                    "visibility_source": "LinkedIn, email list",
                    "differentiator": "Custom 90-day finance roadmaps + business credit setup",
                    "focus_area": "Lead Generation",
                    "revenue": 12000,
                    "blocks": "Low lead conversion from current ads",
                    "client_type": "6-figure coaches and consultants",
                    "team": "Small team",
                    "vision": "Launch a premium mastermind and license tools"
                }

    # Load session state or defaults
    def autofill_value(field, default=""):
        return st.session_state.get("autofill", {}).get(field, default)

    st.markdown("---")
    st.subheader("Step 1: Tell us about your business")

    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business Name", value=autofill_value("business_name"))
        business_type = st.text_area("What does your business do?", value=autofill_value("business_type"))
        audience = st.text_input("Who is your audience?", value=autofill_value("audience"))
        goal = st.text_input("Main Goal", value=autofill_value("goal"))
        budget = st.number_input("Monthly Budget", min_value=0, value=autofill_value("budget", 0))
    with col2:
        market_scope = st.selectbox("Market Scope", ["Local", "Online", "Nationwide", "Global"],
                                     index=["Local", "Online", "Nationwide", "Global"].index(autofill_value("market_scope", "Online")))
        stage = st.selectbox("Business Stage", ["Just starting", "Growing", "Already successful"],
                             index=["Just starting", "Growing", "Already successful"].index(autofill_value("stage", "Just starting")))
        visibility_source = st.text_area("Where do leads currently come from?", value=autofill_value("visibility_source"))
        differentiator = st.text_area("What makes your business different?", value=autofill_value("differentiator"))
        focus_area = st.selectbox("Primary Support Area", 
                                  ["Branding", "Marketing", "Business Development", "Pricing", "Lead Generation", "Client Journey", "Strategy Clarity"],
                                  index=["Branding", "Marketing", "Business Development", "Pricing", "Lead Generation", "Client Journey", "Strategy Clarity"].index(
                                      autofill_value("focus_area", "Strategy Clarity")))

    # Scaling logic
    revenue = blocks = client_type = team = vision = ""
    if stage == "Already successful":
        st.subheader("Growth-Level Strategy Enhancer")
        revenue = st.number_input("Monthly Revenue", min_value=0, value=autofill_value("revenue", 0))
        blocks = st.text_area("Current Growth Challenges", value=autofill_value("blocks"))
        client_type = st.text_input("Ideal Client Type", value=autofill_value("client_type"))
        team = st.selectbox("Team Size", ["Solo", "Small team", "Full agency"],
                            index=["Solo", "Small team", "Full agency"].index(autofill_value("team", "Solo")))
        vision = st.text_area("What does 'next level' look like?", value=autofill_value("vision"))

    # Optional Email
    email_enabled = st.checkbox("✅ Email me this strategy report")
    user_email = st.text_input("Enter email:") if email_enabled else None

    # Submit
    if st.button("🚀 Generate My Genius Strategy"):
        # GPT Prompt Assembly
        gpt_prompt = f"""
        Act as a top-tier business consultant trained in management, marketing, branding, business development, network building, and       mindset coaching. Respond like a Pulitzer-level strategist.

        Business Name: {business_name}
        Description: {business_type}
        Audience: {audience}
        Goal: {goal}
        Budget: {budget}
        Market: {market_scope}
        Stage: {stage}
        Visibility Source: {visibility_source}
        Differentiator: {differentiator}
        Focus Area: {focus_area}
        Revenue: {revenue}
        Growth Blocks: {blocks}
        Ideal Clients: {client_type}
        Team Size: {team}
        Vision: {vision}

        Return a full strategy guide with:
         - Brand and marketing plan
         - Offer structure
         - Funnel or conversion strategy
         - Business credit tips
         - Letter from their future successful self
         - Action steps across the 5 consulting areas (Mindset, Marketing, Branding, Business Development, Network Building)
         - Personalized recommendations for Find Your Way tools the client should use next:
          - Find Your Way Academy
          - Unshakable Self system
          - 21-Day Peak Mode Challenge
          - Credit Repair Tool
          - AI Goal Dashboard
          - Relevant AI Suite tabs (based on their goals and challenges)

          Speak directly to the client as if this is their customized strategy roadmap.
          """


        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        gpt_output_text = response.choices[0].message.content
        st.markdown("---")
        st.subheader("📘 Your Strategy Report")
        st.write(gpt_output_text)

        # PDF Export
        pdf_buffer = io.BytesIO()
        pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, height - 40, "Your Business Genius Strategy Report")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")
        text = pdf.beginText(50, height - 90)
        text.setFont("Helvetica", 10)
        for line in gpt_output_text.split("\n"):
            text.textLine(line)
        pdf.drawText(text)
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button("📄 Download Strategy as PDF", data=pdf_buffer, file_name="Business_Genius_Strategy.pdf")

        # Email Sending
        if email_enabled and user_email:
            email_sent = send_email(
                recipient_email=user_email,
                subject="Your Business Genius Strategy Report",
                body=gpt_output_text,
                sender_email=st.secrets["smtp_user"],
                sender_password=st.secrets["smtp_password"]
            )
            if email_sent:
                st.success("📬 Strategy sent to your email!")
            else:
                st.error("❌ Failed to send email.")

# Required for standalone testing (optional if loaded via main app)
if __name__ == "__main__":
    run()

