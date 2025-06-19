import streamlit as st
from openai import OpenAI
import io
import datetime
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
    Use this tool to reflect, reframe, and reset your mindset.

    1. Choose what you need most today (e.g., focus, confidence).
    2. Write a thought or question you're wrestling with.
    3. Click "Generate Insight" to receive a mindset reframe and advice.
    4. Use the "Message to Future Self" section for vision-building.

    ✅ You can download or email your insights for future reference.
    """)

    st.markdown("#### 🔁 1. Today I Need...")
    need = st.radio(
        "Select what you want to activate today:",
        [
            "🧘‍♂️ Inner Peace & Focus",
            "💪 Confidence & Power",
            "🎯 Discipline & Motivation",
            "🧠 Wisdom & Strategic Thinking",
            "❤️ Healing & Self-Forgiveness"
        ],
        horizontal=True
    )

    if st.button("🔮 Suggest Smart Thought"):
        st.session_state["input_text"] = {
            "🧘‍♂️ Inner Peace & Focus": "I feel distracted and want to slow down my thoughts.",
            "💪 Confidence & Power": "Lately I’ve been second-guessing myself.",
            "🎯 Discipline & Motivation": "I’ve been procrastinating too much.",
            "🧠 Wisdom & Strategic Thinking": "I’m at a crossroads and unsure which direction to take.",
            "❤️ Healing & Self-Forgiveness": "I can’t stop replaying past mistakes."
        }.get(need, "")

    input_text = st.text_area("📝 What's on your mind?", value=st.session_state.get("input_text", ""), height=150)
    user_email = st.text_input("📧 Enter your email to receive insights (optional)")

    if st.button("💡 Generate Insight"):
        base_prompt = f"""
        Act as a motivational life coach helping someone practice emotional awareness and cognitive reframing.

        Their focus today is: {need}
        Their journal input: {input_text}

        Respond with:
        1. A short, empowering mindset shift (reframe)
        2. A micro-action they can take today
        3. One supportive affirmation

        Label each part clearly.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": base_prompt}]
            )
            insight = response.choices[0].message.content
            st.session_state["insight_output"] = insight

            st.markdown("### 🌟 GPT Insight")
            st.write(insight)

            save_data("Self Enhancement", {
                "Date": str(datetime.date.today()),
                "Need": need,
                "Thought": input_text,
                "Response": insight
            })

        except Exception as e:
            st.error(f"GPT Error: {e}")

    # Display output if available
    if "insight_output" in st.session_state:
        st.markdown("### 🌟 GPT Insight")
        st.write(st.session_state["insight_output"])

        if st.download_button("📄 Download PDF", io.BytesIO(create_pdf(st.session_state["insight_output"])), file_name="self_enhancement.pdf"):
            pass

        if user_email and st.button("📬 Email This Insight"):
            email_sent = send_email(
                recipient_email=user_email,
                subject="🧠 Your Self Enhancement Insight",
                body=st.session_state["insight_output"],
                sender_email=st.secrets["email"]["smtp_user"],
                sender_password=st.secrets["email"]["smtp_password"]
            )
            if email_sent:
                st.success("📬 Sent to your email!")
            else:
                st.error("❌ Failed to send email.")

    st.markdown("---")
    st.subheader("📬 Message to My Future Self")

    future_note = st.text_area("What would you like to tell your future self?", key="future_note", height=150)

    if st.button("🔁 Get Future Self Response"):
        try:
            fs_prompt = f"""
            Respond as their wiser, future self (2 years ahead).
            They wrote: {future_note}

            Give a message of reassurance, perspective, and one request they’d thank themselves for doing today.
            Sign off as “Your Future Self”.
            """
            fs_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": fs_prompt}]
            )
            fs_output = fs_response.choices[0].message.content
            st.session_state["fs_output"] = fs_output

            save_data("Self Enhancement", {
                "Date": str(datetime.date.today()),
                "Future Message": future_note,
                "Future Response": fs_output
            })

        except Exception as e:
            st.error(f"GPT Error: {e}")

    if "fs_output" in st.session_state:
        st.markdown("### 📜 Future Self Message")
        st.write(st.session_state["fs_output"])

        if st.download_button("📄 Download Future Self PDF", io.BytesIO(create_pdf(st.session_state["fs_output"])), file_name="future_self.pdf"):
            pass

        if user_email and st.button("📩 Email Future Self Message"):
            email_sent = send_email(
                recipient_email=user_email,
                subject="📬 Message from Your Future Self",
                body=st.session_state["fs_output"],
                sender_email=st.secrets["email"]["smtp_user"],
                sender_password=st.secrets["email"]["smtp_password"]
            )
            if email_sent:
                st.success("✅ Sent your future message!")
            else:
                st.error("❌ Failed to send email.")

def create_pdf(text):
    buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 50, "Self Reflection")
    pdf.setFont("Helvetica", 10)
    t = pdf.beginText(50, height - 80)
    for line in text.split("\n"):
        t.textLine(line)
    pdf.drawText(t)
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == "__main__":
    run()
