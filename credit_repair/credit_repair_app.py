
import streamlit as st
from openai import OpenAI
from utils.send_email import send_email  # Ensure this import works in your structure

client = OpenAI(api_key=st.secrets["openai_api_key"])

def run():
    st.set_page_config(page_title="Credit Repair Tool", layout="wide")
    st.title("📈 Credit Repair & Business Credit Insights")

    # Sidebar Educational Guide
    st.sidebar.title("🧠 Credit Coaching Tips")
    st.sidebar.markdown("""
    Welcome to your virtual **Credit Repair Coach**.

    **What to do here:**
    - Enter any questions, credit issues, or goals.
    - Click **Generate AI Suggestions** to get a personalized action plan.
    - Export results via email if needed.

    **Topics You Can Ask About:**
    - Personal credit repair steps
    - Business credit building
    - How to improve score
    - Secured credit cards
    - Removing collections or inquiries
    - Net-30 vendors or DUNS setup

    **Credit Report Tool:**  
    👉 [findyourwaynmc.creditmyreport.com](https://findyourwaynmc.creditmyreport.com)

    **Learn More:** Visit [FindYourWayNMC.com](https://findyourwaynmc.com) for credit education, funding tools, and step-by-step support.
    """)

    st.markdown("### 💬 What do you need help with?")
    credit_issue = st.text_area("Describe your credit goals, issues, or questions:", placeholder="e.g. I want to build business credit while fixing old collections on my personal report...")

    if st.button("⚡ Generate AI Suggestions"):
        if credit_issue.strip():
            prompt = f"""
You are a professional credit repair and funding advisor. Based on the user's message, provide a structured plan for both personal and business credit. Include steps for building credit, disputing errors, and financial discipline. Include encouragement.

User input:
{credit_issue}

Response:
"""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a top-tier credit repair and business funding strategist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            ai_suggestion = response.choices[0].message.content
            st.session_state["credit_ai_response"] = ai_suggestion
            st.success("✅ Insight generated!")
            st.markdown("### 🧾 Your AI-Generated Credit Action Plan:")
            st.write(ai_suggestion)
        else:
            st.warning("⚠️ Please enter a credit issue or goal before generating.")

    # Show AI result if it exists
    if "credit_ai_response" in st.session_state:
        st.markdown("### 📤 Email Your Plan")
        email = st.text_input("Enter your email to receive this action plan:", key="credit_email")
        if st.button("📧 Send to Email", key="send_credit_email") and email:
            try:
                email_sent = send_email(
                    subject="Your Credit Repair Plan",
                    body=st.session_state["credit_ai_response"],
                    recipient_email=email,
                    sender_email=st.secrets["email"]["smtp_user"],
                    sender_password=st.secrets["email"]["smtp_password"]
                )
                if email_sent:
                    st.success("✅ Plan sent to your email.")
                else:
                    st.error("❌ Failed to send email.")
            except Exception as e:
                st.error(f"Email Error: {e}")

    st.divider()

    # 🔗 Existing Tool/Button (keep as is)
    st.markdown("### 🔧 Credit Consultation & Report Link")
    st.markdown("""
If you need help pulling your full credit report and scheduling a consultation:

👉 [Click here to visit our trusted portal](https://findyourwaynmc.creditmyreport.com)

Here you can:
- Pull your **3-bureau** credit report
- Get personalized help from our team
- Begin your credit transformation journey
""")
