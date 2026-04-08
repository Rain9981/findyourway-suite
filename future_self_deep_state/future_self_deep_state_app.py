import streamlit as st
import datetime
import io
from openai import OpenAI
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from backend.email_utils import send_email


def build_future_self_prompt(
    current_situation,
    desired_future,
    biggest_fears,
    avoided_actions,
    identity_now,
    identity_next,
    urgency,
    focus_area,
    support_system,
    legacy_vision,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in its most advanced form: visionary, psychologically sharp, scholar-level, strategically exact, and deeply confronting in a useful way.

You are not a generic mindset coach.
You are an elite future-self strategist, identity analyst, fear interpreter, and transformation architect.

Your job:
- read the user's current reality honestly
- identify the deeper identity pattern they are living in
- reveal the fear structure shaping their decisions
- project the future they are creating if nothing changes
- speak directly as the future self in at least one section
- recommend exact FYW tools, modules, programs, or tabs if they fit
- explain why upgrading within FYW InterNetwork could help this person specifically
- connect the user's situation to Legacy Architecture when appropriate
- if a recommendation outside FYW is needed, say so honestly

Tone requirements:
- intelligent
- elevated
- emotionally real
- visionary
- psychologically precise
- not theatrical
- not shallow
- not cliché

The output should feel like a mirror, a warning, a map, and a transmission from the user's future self.

Return the response in this exact structure:

1. Deep State Read
2. Identity Pattern Analysis
3. Fear Architecture
4. If Nothing Changes
5. Future Self Transmission
6. Strategic Contradictions
7. Immediate Shift Requirements
8. FYW Program and Tool Match
9. InterNetwork Upgrade Reason
10. Legacy Architecture Connection
11. External Strategic Recommendations
12. Final Mirror Statement

User Inputs:

Current Situation:
{current_situation}

Desired Future:
{desired_future}

Biggest Fears:
{biggest_fears}

What They Keep Avoiding:
{avoided_actions}

Current Identity:
{identity_now}

Desired Identity:
{identity_next}

Urgency / Timeline:
{urgency}

Primary Focus Area:
{focus_area}

Current Support System:
{support_system}

Legacy Vision:
{legacy_vision}

Optional Additional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools / ecosystem to use when appropriate:
- Consulting Guide
- Brand Positioning
- Business Development
- Strategy Designer
- Business Model Canvas
- Business Genius Engine
- Lead Generation
- Marketing Hub
- Marketing Planner
- Email Marketing
- Sentiment Analysis
- Mastermind Analyzer
- Operations Audit
- Oops Audit
- Self Enhancement
- Growth
- KPI Tracker
- Forecasting
- Credit Repair
- Canvas
- Legacy Architecture
- FYW InterNetwork membership pathway

Important:
- In section 8, recommend exact FYW tools, tabs, modules, or programs if they clearly fit.
- In section 9, explain why moving upward through InterNetwork could help this person specifically.
- In section 10, explain how Legacy Architecture relates to structure, environment, identity, and long-term build.
- In section 11, include honest outside recommendations if needed such as therapy, coaching, environment change, legal setup, daily systems, journaling, fitness, or accountability.
- Make the output unforgettable, but grounded in the user's actual input.
"""


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🧠 Future Self Deep State")
    st.caption("A visionary identity-shift engine built to expose fear patterns, future trajectory, and the cost of remaining the same.")

    st.sidebar.header("🌌 Deep State Walkthrough")
    st.sidebar.markdown("""
**What this tool does:**
- reads your current identity pattern
- analyzes fear and avoidance
- projects the likely future if nothing changes
- speaks directly from your future self
- gives strategic next moves
- recommends FYW tools, InterNetwork growth paths, and Legacy Architecture where relevant

**Instructions:**
1. Click **🔮 Suggest Deep State Example** if you want a sample.
2. Complete the reflection fields honestly.
3. Add optional deeper notes if relevant.
4. Click **🚀 Generate Deep State Reading**.
5. Download or email the output if needed.

**Pro Tip:** The more honest and specific your inputs are, the more powerful and precise the output becomes.
""")

    if st.button("🔮 Suggest Deep State Example"):
        st.session_state["future_self_autofill"] = {
            "current_situation": "I have strong vision, but my execution is inconsistent. I keep starting big ideas and then shrinking when the pressure gets real. I know I want more, but I still move like someone protecting comfort instead of building power.",
            "desired_future": "I want to become a disciplined builder with real influence, structure, confidence, and wealth. I want my life and business to reflect clarity, leadership, and legacy.",
            "biggest_fears": "I fear wasting my life, failing publicly, becoming responsible for more than I can handle, and discovering that I am less capable than I believe I could be.",
            "avoided_actions": "I avoid consistent execution, stronger visibility, hard strategic decisions, and fully committing to the level I say I want.",
            "identity_now": "I am a visionary with real potential but inconsistent embodiment.",
            "identity_next": "I become a structured, high-level leader who can carry weight and create real legacy.",
            "legacy_vision": "I want to build something meaningful that outlives me and changes the trajectory of others.",
            "optional_notes": "I often feel like I can see a bigger life, but I still negotiate with fear in hidden ways."
        }

    def autofill_value(field, default=""):
        return st.session_state.get("future_self_autofill", {}).get(field, default)

    st.markdown("### 🪞 Deep State Input")

    current_situation = st.text_area(
        "Current Situation",
        value=autofill_value("current_situation"),
        height=140,
        placeholder="Where are you right now in life, business, mindset, money, direction, and reality?"
    )

    desired_future = st.text_area(
        "Desired Future",
        value=autofill_value("desired_future"),
        height=140,
        placeholder="What future are you trying to create? What kind of life, role, level, or reality do you want?"
    )

    biggest_fears = st.text_area(
        "Biggest Fears",
        value=autofill_value("biggest_fears"),
        height=120,
        placeholder="What are you deeply afraid of? Failure, judgment, success, responsibility, visibility, wasted potential, being seen, losing comfort, etc.?"
    )

    avoided_actions = st.text_area(
        "What You Keep Avoiding",
        value=autofill_value("avoided_actions"),
        height=120,
        placeholder="What do you know you should be doing, but keep delaying, resisting, shrinking from, or talking around?"
    )

    col1, col2 = st.columns(2)

    with col1:
        identity_now = st.text_input(
            "Current Identity in One Sentence",
            value=autofill_value("identity_now"),
            placeholder="Example: I am someone with vision but inconsistent execution."
        )

        identity_next = st.text_input(
            "Desired Identity in One Sentence",
            value=autofill_value("identity_next"),
            placeholder="Example: I become a disciplined strategic builder with power, clarity, and leadership."
        )

        urgency = st.selectbox(
            "Urgency / Timeline",
            [
                "No clear timeline",
                "Within 30 days",
                "Within 90 days",
                "Within 6 months",
                "Within 1 year",
                "This is long-term but serious"
            ]
        )

    with col2:
        focus_area = st.selectbox(
            "Primary Focus Area",
            [
                "Identity Shift",
                "Business Growth",
                "Purpose and Direction",
                "Fear and Avoidance",
                "Leadership",
                "Money and Wealth",
                "Legacy Building",
                "Self Mastery",
                "Relationships and Influence",
                "Everything Feels Connected"
            ]
        )

        support_system = st.selectbox(
            "Current Support System",
            [
                "Very weak or almost none",
                "A little support but inconsistent",
                "Some support but not strategic",
                "Strong emotional support only",
                "Strong strategic support",
                "Building one now"
            ]
        )

        legacy_vision = st.text_input(
            "Legacy Vision",
            value=autofill_value("legacy_vision"),
            placeholder="What do you want your life, business, name, or impact to stand for long-term?"
        )

    optional_notes = st.text_area(
        "Optional Deeper Notes",
        value=autofill_value("optional_notes"),
        height=120,
        placeholder="Anything else that matters: habits, emotional patterns, family pressure, business reality, opportunities, shame, regret, dreams, environment, etc."
    )

    email_enabled = st.checkbox("✅ Email me this deep state reading")
    user_email = st.text_input("Enter your email:") if email_enabled else None

    if st.button("🚀 Generate Deep State Reading"):
        required_fields = [
            current_situation.strip(),
            desired_future.strip(),
            biggest_fears.strip(),
            avoided_actions.strip(),
            identity_now.strip(),
            identity_next.strip(),
        ]

        if not all(required_fields):
            st.warning("⚠️ Please complete the main reflection fields before generating.")
        else:
            try:
                with st.spinner("Reading the deeper pattern behind your future..."):
                    prompt = build_future_self_prompt(
                        current_situation=current_situation,
                        desired_future=desired_future,
                        biggest_fears=biggest_fears,
                        avoided_actions=avoided_actions,
                        identity_now=identity_now,
                        identity_next=identity_next,
                        urgency=urgency,
                        focus_area=focus_area,
                        support_system=support_system,
                        legacy_vision=legacy_vision,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in its highest form: scholar-level, visionary, "
                                    "psychologically sharp, strategically exact, and capable of future-self simulation, "
                                    "identity analysis, fear interpretation, and transformational routing."
                                ),
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.85,
                    )

                    output = response.choices[0].message.content
                    st.session_state["future_self_output"] = output

                st.success("✅ Deep State reading generated.")
                st.subheader("🌌 Your Deep State Reading")
                st.markdown(output)

            except Exception as e:
                st.error(f"Error generating output: {e}")

    if "future_self_output" in st.session_state:
        output = st.session_state["future_self_output"]

        st.divider()

        role = st.session_state.get("user_role", "guest")
        st.markdown("### 🔓 Why This Tool Matters")

        if role == "basic":
            st.info(
                "This tool gives you one of the most powerful identity and trajectory readings in the suite. "
                "If your output reveals bigger needs around structure, growth, strategy, business development, or execution, "
                "higher InterNetwork levels can unlock deeper tools and stronger support."
            )
        elif role == "elite":
            st.info(
                "You already have stronger strategic access. If your output points to advanced execution, visibility, "
                "deeper systems, or expanded support, the next level can help you move further."
            )
        elif role == "premium":
            st.info(
                "You already have expanded access. Use this reading to connect identity work to execution, optimization, and scale."
            )
        elif role == "admin":
            st.success(
                "This tool can help diagnose deeper client identity patterns and route them into the right FYW tools, "
                "InterNetwork pathways, and Legacy Architecture support."
            )

        st.markdown("### 🔗 Next Links")
        st.markdown("""
- [Upgrade Through FYW InterNetwork](https://findyourwaynmc.com/internetwork#internetwork-membership)
- [Visit FindYourWayNMC.com](https://findyourwaynmc.com)
- Use the **Consulting Guide** tab if you want help understanding the recommended tools next
""")

        pdf_buffer = io.BytesIO()
        pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, height - 40, "Your Future Self Deep State Report")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")

        text = pdf.beginText(50, height - 90)
        text.setFont("Helvetica", 10)

        for line in output.split("\n"):
            text.textLine(line)

        pdf.drawText(text)
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button(
            "📄 Download Deep State Report as PDF",
            data=pdf_buffer,
            file_name="Future_Self_Deep_State_Report.pdf"
        )

        if email_enabled and user_email:
            if st.button("📧 Send Deep State Reading to My Email"):
                try:
                    sent = send_email(
                        recipient_email=user_email,
                        subject="Your Future Self Deep State Reading",
                        body=output,
                        sender_email=st.secrets["email"]["smtp_user"],
                        sender_password=st.secrets["email"]["smtp_password"]
                    )
                    if sent:
                        st.success("📬 Deep State reading sent to your email!")
                    else:
                        st.error("❌ Failed to send email.")
                except Exception as e:
                    st.error(f"Email Error: {e}")


if __name__ == "__main__":
    run()