import streamlit as st
from openai import OpenAI
import io
import datetime
import json
import gspread
from backend.google_sheets import save_data
from backend.email_utils import send_email
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🌱 Self Enhancement")
    st.markdown("### Explore and elevate your personal and professional growth.")

    st.sidebar.header("💡 Self Enhancement Guide")
    st.sidebar.markdown("""
    This tool is designed to help you reflect, reset, and reconnect with your best self.
    - Use the input or buttons below for quick mental resets
    - Export insights or send them by email
    - Build daily habits through Future Self alignment
    """)

    # --- Toggle: Today I Need
    st.markdown("#### 🔁 Today I Need…")
    toggle_choice = st.radio("Choose a focus for today:",
        ["🧘 Inner Peace & Focus", "💪 Confidence & Power", "🎯 Discipline & Motivation",
         "🧠 Wisdom & Strategic Thinking", "❤️ Healing & Self-Forgiveness"],
        horizontal=True)

    toggle_prompt_map = {
        "🧘 Inner Peace & Focus": "Give me a calming affirmation and action to center my mind today.",
        "💪 Confidence & Power": "Boost my confidence with a power phrase and action prompt.",
        "🎯 Discipline & Motivation": "Help me build discipline today with mindset and action.",
        "🧠 Wisdom & Strategic Thinking": "Share a wise quote and focus prompt for sharper thinking.",
        "❤️ Healing & Self-Forgiveness": "Give me a healing affirmation and self-kindness reminder."
    }

    if st.button("✨ Get Insight", key="today_need"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a mindset coach generating one short affirmation and one mini action prompt."},
                    {"role": "user", "content": toggle_prompt_map[toggle_choice]}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"GPT Error: {e}")

    # --- AI Journal Entry
    st.markdown("#### 📘 AI Journal Entry Expander")
    journal_input = st.text_area("Write a thought, feeling, or struggle:", "")

    if st.button("🔍 Reflect & Reframe", key="journal_reframe") and journal_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a mindset coach helping reframe emotional thoughts and offer a micro-action for growth."},
                    {"role": "user", "content": f"Help me reframe this: {journal_input}"}
                ]
            )
            insight = response.choices[0].message.content.strip()
            st.session_state["journal_insight"] = insight
            st.success(insight)

            # Save to Sheets
            save_data("Self Enhancement", [str(datetime.datetime.now()), st.session_state.get("user_role", "guest"), journal_input, insight])

        except Exception as e:
            st.error(f"GPT Error: {e}")


    # --- Export and Email after Insight is Generated
    if "journal_insight" in st.session_state:
        st.markdown("#### 📤 What would you like to do with this insight?")
    
        if st.button("📄 Export to PDF", key="pdf1"):
           buffer = io.BytesIO()
           c = pdf_canvas.Canvas(buffer, pagesize=letter)
           c.drawString(100, 750, "AI Journal Reflection")
           c.drawString(100, 735, f"Entry: {journal_input[:60]}...")
           c.drawString(100, 720, "Insight:")
           text_object = c.beginText(100, 705)
           for line in st.session_state["journal_insight"].split("\n"):
            text_object.textLine(line)
           c.drawText(text_object)
           c.save()
           buffer.seek(0)
           st.download_button("📄 Download PDF", buffer, file_name="journal_reflection.pdf", key="download_pdf1")

        if st.button("📧 Send to Email", key="email1"):
            email_sent = send_email(
            subject="Your Self Enhancement Insight",
            body=st.session_state["journal_insight"],
            sender_email=st.secrets["email"]["smtp_user"],
            sender_password=st.secrets["email"]["smtp_password"]
        )
        if email_sent:
            st.success("✅ Sent to your email.")
        else:
            st.error("❌ Email failed to send.")


    # --- Future Self
    st.markdown("#### 🧭 Future Self Alignment")
    future_input = st.text_area("Write a short message to your future self:", "")

    if st.button("📬 Ask Future Self", key="future_self") and future_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are the user's wise, future self answering this letter from the future with gratitude, perspective, and encouragement."},
                    {"role": "user", "content": future_input}
                ]
            )
            future_reply = response.choices[0].message.content.strip()
            st.success(future_reply)

            if st.button("🎯 What would your future self thank you for today?"):
                follow_up = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You're the user's future self giving them one clear, powerful thing to do today that they'll be thankful for later."},
                        {"role": "user", "content": "What would you thank me for doing today?"}
                    ]
                )
                st.info(follow_up.choices[0].message.content.strip())

            if st.button("📄 Export Future Self", key="pdf2"):
                buffer = io.BytesIO()
                c = pdf_canvas.Canvas(buffer, pagesize=letter)
                c.drawString(100, 750, "Letter to My Future Self")
                c.drawString(100, 735, f"Entry: {future_input[:60]}...")
                c.drawString(100, 720, "Response:")
                c.drawString(100, 705, future_reply[:80])
                c.save()
                buffer.seek(0)
                st.download_button("Download PDF", buffer, file_name="future_self_letter.pdf")

            if st.button("📧 Email Future Self", key="email2"):
                send_email("Message from Your Future Self", future_reply)
                st.info("✅ Sent to your email.")

        except Exception as e:
            st.error(f"GPT Error: {e}")

    # --- Legacy Input
    st.markdown("### ✍️ Legacy Self-Enhancement Prompt")
    default_prompt = "I want to improve my time management and confidence."

    if "self_enhancement_autofill_triggered" not in st.session_state:
        st.session_state["self_enhancement_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="autofill_button"):
        st.session_state["self_enhancement_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["self_enhancement_autofill_triggered"] else ""

    legacy_input = st.text_area("What area of your self are you improving?", value=input_value, key="legacy_input")

    if st.button("🚀 Run GPT-4o Autofill", key="legacy_run") and legacy_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a personal development coach helping someone enhance their mindset, skills, or habits."},
                    {"role": "user", "content": legacy_input}
                ]
            )
            insight = response.choices[0].message.content.strip()
            st.success(insight)
            save_data("Self Enhancement", [str(datetime.datetime.now()), st.session_state.get("user_role", "guest"), legacy_input, insight])
        except Exception as e:
            st.error(f"GPT Error: {e}")

