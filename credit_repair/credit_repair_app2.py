import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.set_page_config(page_title="Credit Repair Assistant", layout="wide")
    st.title("🧾 Credit Repair Assistant")

    # Sidebar Guidance
    with st.sidebar:
        st.header("📌 Credit Repair Guidance")
        st.markdown("""
        Use this tool to get suggestions for:
        - Personal credit repair steps
        - Business credit building tips
        - Budgeting & debt strategy
        - Credit score recovery ideas

        🔍 Tips:
        - Be honest and specific in your description  
        - Ask for personal or business help  
        - You can email the results to yourself

        ✉️ Only the AI results are emailed (no data saved).
        """)

    # User Input
    st.markdown("### ✍️ What do you need help with?")
    credit_input = st.text_area("Describe your credit situation or goals (e.g., 'I want to rebuild my personal credit' or 'I need help getting business credit')")

    # GPT Button + Output
    if st.button("💡 Generate AI Credit Suggestions"):
        if credit_input.strip() != "":
            try:
                with st.spinner("Thinking like a credit coach..."):
                    prompt = f"""You are a helpful and educated credit advisor. Based on the user's situation below, give step-by-step suggestions for improving their credit — either personal or business (specify which one based on context). Provide actionable steps and educational insight.

User Situation: {credit_input}
"""
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    credit_suggestions = response.choices[0].message.content
                    st.session_state["credit_ai_output"] = credit_suggestions
                    st.success("✅ AI Credit Suggestions Generated:")
                    st.markdown(credit_suggestions)
            except Exception as e:
                st.error(f"Error generating suggestions: {e}")
        else:
            st.warning("⚠️ Please enter a description first.")

    # Email Export
    if "credit_ai_output" in st.session_state:
        st.markdown("### 📤 Email Your AI Suggestions")
        email_input = st.text_input("Enter your email to receive these suggestions:")
        if st.button("📧 Send to My Email") and email_input:
            try:
                email_sent = send_email(
                    subject="Your AI Credit Repair Suggestions",
                    body=st.session_state["credit_ai_output"],
                    recipient_email=email_input,
                    sender_email=st.secrets["email"]["smtp_user"],
                    sender_password=st.secrets["email"]["smtp_password"]
                )
                if email_sent:
                    st.success("✅ Sent to your email.")
                else:
                    st.error("❌ Email failed to send.")
            except Exception as e:
                st.error(f"Email Error: {e}")

    # Original Credit Repair Tool Button + Link (Preserved)
    st.markdown("---")
    st.markdown("### 🔧 Launch Credit Repair Tool")
    if st.button("🔗 Open Tool"):
        st.markdown(
            "[Click here to open the Credit Repair Tool](https://findyourwaynmc.creditmyreport.com)"
        )

