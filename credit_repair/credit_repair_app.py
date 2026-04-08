import streamlit as st
from openai import OpenAI
from backend.email_utils import send_email

client = OpenAI(api_key=st.secrets["openai"]["api_key"])


def build_credit_prompt(
    main_issue,
    credit_focus,
    score_range,
    has_collections,
    late_payments,
    high_utilization,
    inquiry_concerns,
    business_stage,
    funding_goal,
    report_details,
):
    return f"""
You are a professional credit repair, business credit, and funding strategist.

Your job is to give a tailored, specific, non-generic response based on the user's actual details.
Do not give vague motivation-only advice. Listen closely to the inputs and explain what you noticed.

Important:
- This is educational guidance, not legal or financial representation.
- Be practical, clear, and action-oriented.
- Separate personal credit advice from business credit advice when relevant.
- If the user's issue is mostly personal, say that clearly.
- If the user's issue is mostly business credit, say that clearly.
- If both apply, address both.
- If optional report details were provided, use them directly in the analysis.

Return your answer in this exact structure:

1. Situation Summary
2. What Seems to Be Hurting Them Most
3. Immediate Priorities (next 7 days)
4. Personal Credit Action Plan
5. Business Credit Action Plan
6. Funding Readiness Notes
7. What To Avoid
8. Recommended Next FYW Step
9. Encouragement

User Main Input:
{main_issue}

Credit Focus:
{credit_focus}

Current Score Range:
{score_range}

Collections Present:
{has_collections}

Late Payments Present:
{late_payments}

High Utilization / Maxed Cards:
{high_utilization}

Inquiry Concerns:
{inquiry_concerns}

Business Credit Stage:
{business_stage}

Funding Goal:
{funding_goal}

Optional Credit Report / Tradeline Details:
{report_details if report_details.strip() else "None provided"}
"""


def run():
    st.set_page_config(page_title="Credit Repair Tool", layout="wide")
    st.title("📈 Credit Repair & Business Credit Insights")

    st.sidebar.title("🧠 Credit Coaching Tips")
    st.sidebar.markdown("""
Welcome to your virtual **Credit Repair Coach**.

**How to use this tool:**
- Describe your credit goals, problems, or funding needs.
- Add optional details for a more specific analysis.
- Use the optional report section if you want the AI to respond to actual report details.
- Email the final plan to yourself if needed.

**What this tool can help with:**
- Personal credit rebuilding
- Business credit setup and growth
- Collections and late-payment strategy
- Utilization and inquiry concerns
- DUNS, EIN, LLC, and vendor-readiness guidance
- Funding preparation

**Credit Report Tool:**  
👉 [findyourwaynmc.creditmyreport.com](https://findyourwaynmc.creditmyreport.com)

**Learn More:**  
👉 [FindYourWayNMC.com](https://findyourwaynmc.com)
""")

    st.markdown("### 💬 What do you need help with?")
    credit_issue = st.text_area(
        "Describe your credit goals, issues, or questions:",
        placeholder="Example: I want to fix old collections on my personal report while also building business credit for future funding."
    )

    st.markdown("### 🧩 Optional Detail Builder")
    col1, col2 = st.columns(2)

    with col1:
        credit_focus = st.selectbox(
            "What type of help do you need most?",
            ["Both Personal and Business", "Personal Credit", "Business Credit", "Not Sure"]
        )

        score_range = st.selectbox(
            "Current score range (optional estimate)",
            ["Not Sure", "Below 550", "550-599", "600-649", "650-699", "700+"]
        )

        has_collections = st.selectbox(
            "Do you currently have collections?",
            ["Not Sure", "Yes", "No"]
        )

        late_payments = st.selectbox(
            "Do you have late payments showing?",
            ["Not Sure", "Yes", "No"]
        )

    with col2:
        high_utilization = st.selectbox(
            "Are your cards highly utilized or close to maxed out?",
            ["Not Sure", "Yes", "No"]
        )

        inquiry_concerns = st.selectbox(
            "Too many recent inquiries?",
            ["Not Sure", "Yes", "No"]
        )

        business_stage = st.selectbox(
            "Business credit stage",
            [
                "Not Applicable",
                "Just Starting",
                "LLC Formed",
                "Have EIN",
                "Have DUNS / Business Profile",
                "Using Vendors / Net-30 Accounts",
                "Already Building Business Credit"
            ]
        )

        funding_goal = st.text_input(
            "Funding goal (optional)",
            placeholder="Example: I want to qualify for $25,000 in business funding later."
        )

    st.markdown("### 📄 Optional Credit Report / Tradeline Details")
    report_details = st.text_area(
        "Paste report notes, tradelines, collections, balances, inquiries, utilization details, or business credit profile details here (optional):",
        placeholder="Example: 3 collections, 2 cards over 85% utilization, 5 inquiries in 6 months, one 30-day late, LLC formed, EIN active, no DUNS yet."
    )

    if st.button("⚡ Generate AI Suggestions"):
        if credit_issue.strip():
            try:
                with st.spinner("Analyzing your credit situation..."):
                    prompt = build_credit_prompt(
                        main_issue=credit_issue,
                        credit_focus=credit_focus,
                        score_range=score_range,
                        has_collections=has_collections,
                        late_payments=late_payments,
                        high_utilization=high_utilization,
                        inquiry_concerns=inquiry_concerns,
                        business_stage=business_stage,
                        funding_goal=funding_goal,
                        report_details=report_details,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a top-tier credit repair and business funding strategist. "
                                    "Give highly tailored, structured, practical advice based on the user's actual details. "
                                    "Do not be generic."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.5,
                    )

                    ai_suggestion = response.choices[0].message.content
                    st.session_state["credit_ai_response"] = ai_suggestion

                st.success("✅ Insight generated!")
                st.markdown("### 🧾 Your AI-Generated Credit Action Plan:")
                st.markdown(ai_suggestion)

            except Exception as e:
                st.error(f"Error generating suggestions: {e}")
        else:
            st.warning("⚠️ Please enter your main credit issue or goal before generating.")

    if "credit_ai_response" in st.session_state:
        st.divider()
        st.markdown("### 📤 Email Your Plan")
        email = st.text_input(
            "Enter your email to receive this action plan:",
            key="credit_email"
        )

        if st.button("📧 Send to Email", key="send_credit_email"):
            if email.strip():
                try:
                    email_body = f"""Find Your Way Credit Action Plan

Main Issue:
{credit_issue}

AI Plan:
{st.session_state["credit_ai_response"]}
"""
                    email_sent = send_email(
                        recipient_email=email,
                        subject="Your Credit Repair & Business Credit Plan",
                        body=email_body,
                        sender_email=st.secrets["email"]["smtp_user"],
                        sender_password=st.secrets["email"]["smtp_password"],
                    )

                    if email_sent:
                        st.success("✅ Plan sent to your email.")
                    else:
                        st.error("❌ Failed to send email.")
                except Exception as e:
                    st.error(f"Email Error: {e}")
            else:
                st.warning("⚠️ Please enter an email address first.")

    st.divider()

    st.markdown("### 🔧 Credit Consultation & Report Link")
    st.markdown("""
If you want to pull your full credit report and connect it to your next steps:

👉 [Click here to visit our trusted portal](https://findyourwaynmc.creditmyreport.com)

Here you can:
- Pull your **3-bureau** credit report
- Review your profile in more detail
- Take the next step in your credit improvement journey
""")

    st.info(
        "Tip: For the best analysis, enter your main issue first, then add optional report or tradeline details if you have them."
    )