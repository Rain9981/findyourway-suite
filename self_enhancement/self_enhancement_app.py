import streamlit as st
from openai import OpenAI
import io
import datetime
import gspread
from backend.google_sheets import save_data
from backend.email_utils import send_email
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
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

    smart_thoughts = {
        "🧘‍♂️ Inner Peace & Focus": "I feel distracted and want to slow down my thoughts.",
        "💪 Confidence & Power": "Lately I’ve been second-guessing myself.",
        "🎯 Discipline & Motivation": "I’ve been procrastinating too much.",
        "🧠 Wisdom & Strategic Thinking": "I’m at a crossroads and unsure which direction to take.",
        "❤️ Healing & Self-Forgiveness": "I can’t stop replaying past mistakes."
    }

    if st.button("✨ Suggest Smart Thought"):
        st.session_state.input_text = smart_thoughts.get(need, "")

    input_text = st.text_area(
        "📝 What's on your mind?",
        value=st.session_state.get("input_text", ""),
        height=150
    )

    user_email = st.text_input("📧 Enter your email to receive results (optional)")

    if st.button("💡 Generate Insight"):
        prompt = f"""
        Act as a motivational life coach helping someone reframe their thinking.

        Focus: {need}
        Thought: {input_text}

        Respond with:
        - A mindset reframe
        - A micro-action to take today
        - An affirmation

        Label each part clearly.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            output = response.choices[0].message.content

            st.markdown("### 🌟 Reframe Insight")
            st.write(output)

            save_data("Self Enhancement", {
                "Date": str(datetime.date.today()),
                "Need": need,
                "Thought": input_text,
                "Response": output
            })

            if user_email:
                sent = send_email(
                    recipient_email=user_email,
                    subject="🧠 Your Self Enhancement Insight",
                    body=output,
                    sender_email=st.secrets["email"]["smtp_user"],
                    sender_password=st.secrets["email"]["smtp_password"]
                )
                if sent:
                    st.success("📬 Sent to your email!")
                else:
                    st.error("❌ Email failed to send.")

            st.download_button("📄 Download Reflection PDF", io.BytesIO(create_pdf("Self Enhancement Reflection", output)), file_name="reflection.pdf")

        except Exception as e:
            st.error(f"GPT Error: {e}")

    st.markdown("---")
    st.subheader("📬 Message to My Future Self")

    future_note = st.text_area("Write a message to your Future Self:", height=150)

    if st.button("🔁 Get Future Self Response"):
        fs_prompt = f"""
        Respond as the user's future self (2 years ahead). They wrote:

        "{future_note}"

        Give:
        1. A message of reassurance
        2. A wise perspective
        3. One action they’ll thank themselves for doing today

        End the message as: "– Your Future Self"
        """

        try:
            fs_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": fs_prompt}]
            )
            fs_output = fs_response.choices[0].message.content

            st.markdown("### 📜 Future Self Message")
            st.write(fs_output)

            save_data("Self Enhancement", {
                "Date": str(datetime.date.today()),
                "Future Message": future_note,
                "Future Response": fs_output
            })

            if user_email:
                sent = send_email(
                    recipient_email=user_email,
                    subject="📬 Message from Your Future Self",
                    body=fs_output,
                    sender_email=st.secrets["email"]["smtp_user"],
                    sender_password=st.secrets["email"]["smtp_password"]
                )
                if sent:
                    st.success("📩 Future self email sent!")
                else:
                    st.error("❌ Email failed to send.")

            st.download_button("📄 Download Future Self PDF", io.BytesIO(create_pdf("Message from Your Future Self", fs_output)), file_name="future_self.pdf")

        except Exception as e:
            st.error(f"GPT Error: {e}")

def create_pdf(title, body_text):
    buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 50, title)
    pdf.setFont("Helvetica", 10)
    t = pdf.beginText(50, height - 80)
    for line in body_text.split("\n"):
        t.textLine(line.strip())
    pdf.drawText(t)
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == "__main__":
    run()
