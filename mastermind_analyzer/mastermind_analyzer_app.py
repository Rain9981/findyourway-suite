
import streamlit as st
import datetime
import io
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from backend.email_utils import send_email

def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    st.title("🧠 Mastermind Analyzer")
    st.caption("Elite-level insight tool for strategic refinement, rewriting, and vision enhancement.")

    # Sidebar Guide
    st.sidebar.header("🧠 Mastermind Walkthrough")
    st.sidebar.markdown("""
    **What this tool does:**
    - Analyzes your input using high-level consultant logic.
    - Refines tone, expands ideas, or gives feedback like a strategy expert.

    **Instructions:**
    1. Choose your analysis style from the dropdown.
    2. Click 🔄 Suggest Example Input if you want a sample.
    3. Paste or type your content into the large box.
    4. Click 🎯 Run Mastermind Analysis to generate a result.
    5. Export to PDF or email the output if needed.

    **Pro Tip:** This tool works best with full answers, ideas, strategies, or written explanations.
    """)

    # Analysis Type
    analysis_type = st.selectbox("Select Analysis Type", [
        "Strategic Feedback",
        "Rewrite in Expert Tone",
        "Expansion & Ideas",
        "Summarize & Improve"
    ])

    # Autofill button
    if st.button("🔄 Suggest Example Input"):
        st.session_state["mastermind_input"] = (
            "- We currently offer one-on-one coaching, but leads aren't converting.\n"
            "- Considering group coaching but unsure how to position it.\n"
            "- Want to increase high-ticket enrollments."
        )

    user_input = st.text_area("📝 Paste your content or response here", height=300, value=st.session_state.get("mastermind_input", ""))

    email_enabled = st.checkbox("✅ Email me this analysis")
    user_email = st.text_input("Enter your email:") if email_enabled else None

    # Genius Loop Toggle
    followup_enabled = st.checkbox("🔁 Enable Genius Follow-Up Loop")

    if st.button("🎯 Run Mastermind Analysis") and user_input.strip():
        sections = [s.strip() for s in user_input.split("\n") if s.strip()]
        full_output = ""

        for i, section in enumerate(sections, start=1):
            prompt = f""" 
Act as the 'Rain' GPT — a master-level business strategist inside the Find Your Way AI Suite.
Using a confident, intelligent, and visionary tone, perform this analysis:
Type: [{analysis_type}]
Input #{i}:
{section}

Respond as a world-class consultant giving tailored insight.
            """
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            full_output += f"🔹 Insight for Entry {i}:\n{response.choices[0].message.content}\n\n"

        # Follow-up refinement
        if followup_enabled:
            refinement_type = st.selectbox("🔁 Choose refinement style:", [
                "Make more actionable",
                "Add follow-up recommendations",
                "Refine tone to be more persuasive",
                "Simplify for client clarity"
            ])
            followup_prompt = f"""
Take the following strategic insights and refine them using this instruction: [{refinement_type}]

Use elite business consulting tone — intelligent, empowering, and strategic.

--- Begin Original Insights ---
{full_output}
--- End ---
"""
            followup_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": followup_prompt}]
            )
            full_output += "\n🔁 Genius Loop Refinement:\n" + followup_response.choices[0].message.content

        # Display Output
        st.subheader("📘 Mastermind Insight")
        st.write(full_output)

        # PDF Export
        pdf_buffer = io.BytesIO()
        pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, height - 40, "Your Mastermind Analyzer Report")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")
        text = pdf.beginText(50, height - 90)
        text.setFont("Helvetica", 10)
        for line in full_output.split("\n"):
            text.textLine(line)
        pdf.drawText(text)
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button("📄 Download Analysis as PDF", data=pdf_buffer, file_name="Mastermind_Analysis_Report.pdf")

        if email_enabled and user_email:
            sent = send_email(
                recipient_email=user_email,
                subject="Your Mastermind Analyzer Report",
                body=full_output,
                sender_email=st.secrets["email"]["smtp_user"],
                sender_password=st.secrets["email"]["smtp_password"]
            )
            if sent:
                st.success("📬 Analysis sent to your email!")
            else:
                st.error("❌ Failed to send email.")

if __name__ == "__main__":
    run()
