import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_strategic_simulator_prompt(
    scenario_input,
    business_stage,
    priority_focus,
    risk_tolerance,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in strategic simulation mode: commercially sharp, analytical, practical, and clear.

You are not a generic chatbot.
You are a high-level business strategist helping simulate the likely outcomes of a business decision, move, or scenario.

Your job:
- analyze the business scenario
- simulate likely positive outcomes
- simulate likely risks and unintended consequences
- identify what variables matter most
- recommend the smartest next move
- suggest exact FYW tools or tabs when relevant

Tone requirements:
- strategic
- direct
- useful
- polished
- realistic
- not dramatic
- not vague

Return the response in this exact structure:

1. Scenario Snapshot
2. Likely Positive Outcomes
3. Likely Risks and Downsides
4. Key Variables That Will Affect the Outcome
5. Best-Case Scenario
6. Worst-Case Scenario
7. Most Likely Scenario
8. Strategic Recommendation
9. Next Best Actions
10. FYW Tool Match
11. Final Simulation Insight

Scenario Input:
{scenario_input}

Business Stage:
{business_stage}

Priority Focus:
{priority_focus}

Risk Tolerance:
{risk_tolerance}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools / ecosystem:
- Consulting Guide
- Strategy Designer
- Business Development
- Brand Positioning
- Business Genius Engine
- Marketing Hub
- Marketing Planner
- Lead Generation
- KPI Tracker
- Forecasting
- Growth
- Operations Audit
- CRM
- CRM Dashboard
- Canvas
"""


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("♟️ Strategic Simulator")
    st.caption("Simulate business decisions, pressure-test possible outcomes, and get a smarter next move before acting.")

    st.sidebar.header("💡 Strategic Simulator Guide")
    st.sidebar.markdown("""
**What this tool does:**
- simulates possible business outcomes
- helps pressure-test decisions before acting
- reveals upside, downside, and hidden variables
- recommends smarter next steps

**Instructions:**
1. Click **✨ Suggest Simulation Example** if you want a sample.
2. Describe the business scenario you want to test.
3. Select the stage, focus, and risk level.
4. Click **🚀 Run Strategic Simulation**.
5. Download the report if needed.

**Pro Tip:** The more specific the scenario, the more realistic and useful the simulation.
""")

    if st.button("✨ Suggest Simulation Example"):
        st.session_state["strategic_simulator_autofill"] = {
            "scenario_input": "If we lower our product prices by 10%, how might it affect revenue, customer loyalty, perceived value, and repeat purchases over the next 90 days?",
            "business_stage": "Growing",
            "priority_focus": "Revenue Growth",
            "risk_tolerance": "Moderate",
            "optional_notes": "The business wants more customers but does not want to weaken brand positioning."
        }

    def autofill_value(field, default=""):
        return st.session_state.get("strategic_simulator_autofill", {}).get(field, default)

    st.markdown("### 📥 Strategic Simulation Input")

    scenario_input = st.text_area(
        "Describe your business scenario to simulate:",
        value=autofill_value("scenario_input"),
        height=160,
        placeholder="Example: If I raise prices, add a service, hire help, change positioning, start ads, or shift target audience, what is likely to happen?"
    )

    col1, col2 = st.columns(2)

    stage_options = ["Startup", "Growing", "Established", "Scaling"]
    focus_options = [
        "Revenue Growth",
        "Lead Generation",
        "Brand Positioning",
        "Operational Efficiency",
        "Customer Retention",
        "Market Expansion"
    ]
    risk_options = ["Low", "Moderate", "High"]

    with col1:
        business_stage = st.selectbox(
            "Business Stage",
            stage_options,
            index=stage_options.index(autofill_value("business_stage", "Growing")) if autofill_value("business_stage", "Growing") in stage_options else 1
        )

        priority_focus = st.selectbox(
            "Priority Focus",
            focus_options,
            index=focus_options.index(autofill_value("priority_focus", "Revenue Growth")) if autofill_value("priority_focus", "Revenue Growth") in focus_options else 0
        )

    with col2:
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            risk_options,
            index=risk_options.index(autofill_value("risk_tolerance", "Moderate")) if autofill_value("risk_tolerance", "Moderate") in risk_options else 1
        )

    optional_notes = st.text_area(
        "Optional Notes",
        value=autofill_value("optional_notes"),
        height=120,
        placeholder="Anything else that matters: competition, budget, timing, current customer behavior, internal concerns, etc."
    )

    if st.button("🚀 Run Strategic Simulation"):
        if not scenario_input.strip():
            st.warning("⚠️ Please enter a scenario before running the simulation.")
        else:
            try:
                with st.spinner("Simulating strategic outcomes..."):
                    prompt = build_strategic_simulator_prompt(
                        scenario_input=scenario_input,
                        business_stage=business_stage,
                        priority_focus=priority_focus,
                        risk_tolerance=risk_tolerance,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are Rain Intelligence in strategic simulation mode: sharp, executive, realistic, and commercially intelligent."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["strategic_simulator_result"] = output

                    try:
                        save_data("Strategic_Simulator", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Scenario_Input": scenario_input,
                            "Business_Stage": business_stage,
                            "Priority_Focus": priority_focus,
                            "Risk_Tolerance": risk_tolerance,
                            "Optional_Notes": optional_notes,
                            "Simulation_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Simulation generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Strategic simulation generated.")
                st.subheader("♟️ Strategic Simulation Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if "strategic_simulator_result" in st.session_state:
        output = st.session_state["strategic_simulator_result"]

        pdf_buffer = io.BytesIO()
        pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, height - 40, "Strategic Simulation Report")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 60, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}")

        text = pdf.beginText(50, height - 90)
        text.setFont("Helvetica", 10)

        y_position = height - 90
        for line in output.split("\n"):
            if y_position < 50:
                pdf.drawText(text)
                pdf.showPage()
                text = pdf.beginText(50, height - 50)
                text.setFont("Helvetica", 10)
                y_position = height - 50
            text.textLine(line)
            y_position -= 12

        pdf.drawText(text)
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button(
            "📄 Download Strategic Simulation Report as PDF",
            data=pdf_buffer,
            file_name="Strategic_Simulation_Report.pdf"
        )


if __name__ == "__main__":
    run()