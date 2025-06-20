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
            save_data("Self Enhancement", {
                "Timestamp": str(datetime.datetime.now()),
                "User Role": st.session_state.get("user_role", "guest"),
                "Journal Entry": journal_input,
                "AI Insight": insight
            })


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

    # --- Journal Insight Email Field + Send
    st.markdown("#### 📧 Email Your Insight")

    user_email = st.text_input("Enter your email address:", key="journal_email")

    if st.button("📧 Send to Email", key="email1") and user_email:
        try:
            email_sent = send_email(
                subject="Your Self Enhancement Insight",
                body=st.session_state["journal_insight"],
                sender_email=st.secrets["email"]["smtp_user"],
                sender_password=st.secrets["email"]["smtp_password"],
                recipient_email=user_email
            )
            if email_sent:
                st.success("✅ Sent to your email.")
            else:
                st.error("❌ Email failed to send.")
        except Exception as e:
            st.error(f"Email Error: {e}")



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
            st.session_state["future_reply"] = future_reply  # <-- you forgot this line too
        except Exception as e:
            st.error(f"GPT Error: {e}")

    # Only show this if a future_input was already processed
    if "future_reply" in st.session_state:
        st.markdown("##### 🔄 Optional: What would your future self thank you for today?")
    
    # Future Self Thank You Button
    if st.button("🎯 Get Thank You Action", key="future_thankyou"):
        try:
            follow_up = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're the user's future self giving them one clear, powerful thing to do today that they'll be thankful for later."},
                    {"role": "user", "content": "What would you thank me for doing today?"}
                ]
            )
            thank_you = follow_up.choices[0].message.content.strip()
            st.session_state["future_thank_you"] = thank_you
            st.success(thank_you)
        except Exception as e:
            st.error(f"GPT Error: {e}")


    # Display PDF and Email buttons only if thank_you is stored
    if "future_thank_you" in st.session_state:
        # PDF Export
        if st.button("📄 Export Future Self", key="pdf2"):
            buffer = io.BytesIO()
            c = pdf_canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, "Letter to My Future Self")
            c.drawString(100, 735, f"Entry: {future_input[:60]}...")
            c.drawString(100, 720, "Response:")
            text_obj = c.beginText(100, 705)
            for line in st.session_state["future_thank_you"].split("\n"):
                text_obj.textLine(line)
            c.drawText(text_obj)
            c.save()
            buffer.seek(0)
            st.download_button("📄 Download PDF", buffer, file_name="future_self_letter.pdf", key="download_pdf2")

    # Email Input + Send
    recipient_email_2 = st.text_input("Enter your email to receive this letter:", key="future_email_input")
    if st.button("📧 Email Future Self", key="email2") and recipient_email_2:
        try:
            email_sent = send_email(
                subject="Letter from Your Future Self",
                body=st.session_state["future_thank_you"],
                recipient_email=recipient_email_2,
                sender_email=st.secrets["email"]["smtp_user"],
                sender_password=st.secrets["email"]["smtp_password"]
            )
            if email_sent:
                st.success("✅ Sent to your email.")
            else:
                st.error("❌ Email failed to send.")
        except Exception as e:
            st.error(f"Email Error: {e}")

    # --- Legacy Input
    st.markdown("### ✍️ Legacy Self-Enhancement Prompt")
    default_prompt = "I want to improve my time management and confidence."

    if "self_enhancement_autofill_triggered" not in st.session_state:
        st.session_state["self_enhancement_autofill_triggered"] = False

    if st.button("✨ Autofill Suggestion", key="autofill_button"):
       st.session_state["self_enhancement_autofill_triggered"] = True

    input_value = default_prompt if st.session_state["self_enhancement_autofill_triggered"] else ""

    legacy_input = st.text_area("What area of your self are you improving?", value=input_value, key="legacy_input")
    
    # --- GPT Autofill + Insight (Legacy)
    if st.button("🚀 Run GPT-4o Autofill", key="legacy_gpt"):
    with st.spinner("Thinking..."):
        try:
            prompt = f"Reflect on this legacy question and give insight:\n{legacy_input}"
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a wise legacy coach helping someone connect with their long-term impact and legacy."},
                    {"role": "user", "content": prompt}
                ]
            )
            insight = completion.choices[0].message.content.strip()
            st.session_state["legacy_insight"] = insight
        except Exception as e:
            st.error(f"GPT Error: {e}")

# --- Show Insight if exists
if "legacy_insight" in st.session_state:
    insight = st.session_state["legacy_insight"]
    st.markdown("### 💡 Legacy Insight")
    st.success(insight)

    # --- Export: PDF
    if st.button("📄 Download PDF", key="legacy_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        text = c.beginText(50, 750)
        text.setFont("Helvetica", 12)
        text.textLines(f"Legacy Self-Reflection:\n{legacy_input}\n\nGPT Insight:\n{insight}")
        c.drawText(text)
        c.save()
        buffer.seek(0)
        st.download_button(
            label="📥 Download Legacy Insight PDF",
            data=buffer,
            file_name="legacy_insight.pdf",
            mime="application/pdf",
        )

    # --- Export: Email
    st.markdown("#### 📬 Email Insight")
    recipient_email_legacy = st.text_input("Enter your email:", key="email_legacy")

    if st.button("📤 Email This Insight", key="send_legacy_email") and recipient_email_legacy:
        try:
            email_subject = "Your Legacy Self-Enhancement Insight"
            email_body = f"Reflection:\n{legacy_input}\n\nAI Insight:\n{insight}"
            email_sent = send_email(
                subject=email_subject,
                body=email_body,
                recipient_email=recipient_email_legacy,
                sender_email=st.secrets["email"]["smtp_user"],
                sender_password=st.secrets["email"]["smtp_password"]
            )
            if email_sent:
                st.success("✅ Insight emailed successfully.")
            else:
                st.error("❌ Email failed to send.")
        except Exception as e:
            st.error(f"Email Error: {e}")
    