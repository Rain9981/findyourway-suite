import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_oops_prompt(issue, impact, cause, audience_affected, recovery_goal, lesson_focus, urgency, optional_notes):
    return f"""
Act as Rain Intelligence in mistake recovery and strategic audit mode: direct, constructive, practical, and business-focused.

Return this exact structure:

1. Situation Snapshot
2. What Went Wrong
3. Root Cause Analysis
4. Business Impact
5. Audience / Customer Trust Risk
6. Recovery Strategy
7. Prevention System
8. Lesson to Capture
9. FYW Tool Match
10. Next Best Actions
11. Final Recovery Insight

Issue / Mistake:
{issue}

Impact:
{impact}

Likely Cause:
{cause}

Audience Affected:
{audience_affected}

Recovery Goal:
{recovery_goal}

Lesson Focus:
{lesson_focus}

Urgency:
{urgency}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}
"""


def create_pdf_buffer(title, output):
    buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 40, title)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")
    text = pdf.beginText(50, height - 90)
    text.setFont("Helvetica", 10)
    y = height - 90
    for line in output.split("\n"):
        if y < 50:
            pdf.drawText(text)
            pdf.showPage()
            text = pdf.beginText(50, height - 50)
            text.setFont("Helvetica", 10)
            y = height - 50
        text.textLine(line[:110])
        y -= 12
    pdf.drawText(text)
    pdf.save()
    buffer.seek(0)
    return buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🚨 Oops Audit")
    st.caption("Turn business mistakes, failures, and setbacks into recovery plans, lessons, and prevention systems.")

    st.sidebar.header("💡 Oops Audit Guide")
    st.sidebar.markdown("""
**What this tool does:**
- audits mistakes or business setbacks
- identifies likely root causes
- creates a recovery and prevention plan
- turns failure into strategy

**Best use:**
Use when something went wrong and you need to recover professionally.

**Pro Tip:** The goal is not blame. The goal is pattern recognition, recovery, and better systems.
""")

    defaults = {
        "oops_issue": "",
        "oops_impact": "",
        "oops_cause": "",
        "oops_audience": "",
        "oops_recovery_goal": "",
        "oops_optional_notes": "",
        "oops_lesson_focus": "Process Improvement",
        "oops_urgency": "Moderate",
        "oops_audit_result": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.button("✨ Autofill Example"):
        st.session_state["oops_issue"] = "We launched a new offer without testing the messaging, and the response was weak."
        st.session_state["oops_impact"] = "Low conversions, wasted time, and reduced confidence in the campaign."
        st.session_state["oops_cause"] = "We rushed the launch without validating the audience pain point, offer clarity, or CTA."
        st.session_state["oops_audience"] = "Past leads and social media audience."
        st.session_state["oops_recovery_goal"] = "Recover trust, improve the offer message, and relaunch with a stronger strategy."
        st.session_state["oops_lesson_focus"] = "Marketing / Messaging"
        st.session_state["oops_urgency"] = "Moderate"
        st.session_state["oops_optional_notes"] = "We want to avoid looking inconsistent or unprepared."

    st.markdown("### 📥 Oops Audit Input")

    issue = st.text_area("What went wrong?", key="oops_issue", height=100)
    impact = st.text_area("What was the impact?", key="oops_impact", height=90)
    cause = st.text_area("What do you think caused it?", key="oops_cause", height=90)
    audience_affected = st.text_area("Who was affected?", key="oops_audience", height=80)
    recovery_goal = st.text_area("Recovery Goal", key="oops_recovery_goal", height=80)

    col1, col2 = st.columns(2)
    with col1:
        lesson_focus = st.selectbox(
            "Lesson Focus",
            ["Process Improvement", "Marketing / Messaging", "Customer Experience", "Leadership", "Operations", "Sales / Conversion", "Brand Trust"],
            key="oops_lesson_focus"
        )
    with col2:
        urgency = st.selectbox("Urgency", ["Low", "Moderate", "High"], key="oops_urgency")

    optional_notes = st.text_area("Optional Notes", key="oops_optional_notes", height=90)

    if st.button("🚀 Generate Oops Audit"):
        required = [issue.strip(), impact.strip(), cause.strip(), recovery_goal.strip()]
        if not all(required):
            st.warning("⚠️ Please complete the main audit fields before generating.")
        else:
            try:
                with st.spinner("Auditing issue and building recovery strategy..."):
                    prompt = build_oops_prompt(issue, impact, cause, audience_affected, recovery_goal, lesson_focus, urgency, optional_notes)

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are Rain Intelligence in business recovery audit mode: direct, constructive, practical, and strategic."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.75,
                    )

                    output = response.choices[0].message.content
                    st.session_state["oops_audit_result"] = output

                    try:
                        save_data("Oops_Audit", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Issue": issue,
                            "Impact": impact,
                            "Cause": cause,
                            "Audience_Affected": audience_affected,
                            "Recovery_Goal": recovery_goal,
                            "Lesson_Focus": lesson_focus,
                            "Urgency": urgency,
                            "Optional_Notes": optional_notes,
                            "Audit_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Oops audit generated.")
                st.subheader("🚨 Oops Audit Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("oops_audit_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Oops Audit Report", st.session_state["oops_audit_result"])
        st.download_button("📄 Download Oops Audit Report", pdf_buffer, file_name="Oops_Audit_Report.pdf")


if __name__ == "__main__":
    run()