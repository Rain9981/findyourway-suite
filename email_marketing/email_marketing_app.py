import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data


def build_email_prompt(
    audience,
    goal,
    offer,
    tone,
    email_type,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in conversion-focused email marketing mode.

Return:

1. Subject Line Options
2. Opening Hook
3. Email Body
4. Call To Action
5. Follow-Up Idea

Audience: {audience}
Goal: {goal}
Offer: {offer}
Tone: {tone}
Email Type: {email_type}
Notes: {optional_notes}
"""


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("📬 Email Marketing V2")
    st.caption("Create high-converting marketing emails.")

    if "email_result" not in st.session_state:
        st.session_state["email_result"] = ""

    if st.button("✨ Autofill Example"):
        st.session_state.update({
            "email_audience": "Past leads",
            "email_goal": "Drive conversions",
            "email_offer": "Coaching program",
            "email_tone": "Persuasive",
            "email_type": "Promotional",
            "email_notes": "Warm but direct"
        })

    audience = st.text_area("Audience", key="email_audience")
    goal = st.text_area("Goal", key="email_goal")
    offer = st.text_area("Offer", key="email_offer")

    col1, col2 = st.columns(2)

    with col1:
        tone = st.selectbox("Tone", ["Persuasive", "Warm", "Urgent", "Professional"], key="email_tone")

    with col2:
        email_type = st.selectbox("Type", ["Promotional", "Follow-Up", "Welcome", "Re-engagement"], key="email_type")

    optional_notes = st.text_area("Notes", key="email_notes")

    if st.button("🚀 Generate Email"):
        prompt = build_email_prompt(audience, goal, offer, tone, email_type, optional_notes)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content
        st.session_state["email_result"] = output

        save_data("Email_Marketing", {"Result": output})

        st.success(output)