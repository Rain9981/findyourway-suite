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


def create_pdf_buffer(title, output):
    pdf_buffer = io.BytesIO()
    pdf = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 40, title)

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
        text.textLine(line[:110])
        y_position -= 12

    pdf.drawText(text)
    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("♟️ Strategic Simulator")
    st.caption(
        "Simulate business decisions, pressure-test possible outcomes, and get a smarter next move before acting."
    )

    st.sidebar.header("💡 Strategic Simulator Guide")
    st.sidebar.markdown("""
**What this tool does:**
- simulates possible business outcomes
- helps pressure-test decisions before acting
- reveals upside, downside, and hidden variables
- scores strategy strength using key business indicators
- recommends smarter next steps

**Simulation Modes:**
1. **Scenario Simulation** — describe a decision and receive a strategic AI breakdown.
2. **Strategic Score Simulation** — use sliders to calculate a directional strategy score.

**Pro Tip:** Use Scenario Simulation for deeper thinking. Use Strategic Score Simulation for quick decision pressure-testing.
""")

    # -------------------------
    # Session state defaults
    # -------------------------
    if "scenario_input" not in st.session_state:
        st.session_state["scenario_input"] = ""

    if "business_stage" not in st.session_state:
        st.session_state["business_stage"] = "Growing"

    if "priority_focus" not in st.session_state:
        st.session_state["priority_focus"] = "Revenue Growth"

    if "risk_tolerance" not in st.session_state:
        st.session_state["risk_tolerance"] = "Moderate"

    if "optional_notes" not in st.session_state:
        st.session_state["optional_notes"] = ""

    if "strategic_simulator_result" not in st.session_state:
        st.session_state["strategic_simulator_result"] = ""

    mode = st.radio(
        "Choose Simulation Mode",
        ["Scenario Simulation", "Strategic Score Simulation"],
        horizontal=True
    )

    # -------------------------
    # MODE 1: GPT Scenario Simulation
    # -------------------------
    if mode == "Scenario Simulation":
        if st.button("✨ Suggest Simulation Example"):
            st.session_state["scenario_input"] = (
                "If we lower our product prices by 10%, how might it affect revenue, "
                "customer loyalty, perceived value, and repeat purchases over the next 90 days?"
            )
            st.session_state["business_stage"] = "Growing"
            st.session_state["priority_focus"] = "Revenue Growth"
            st.session_state["risk_tolerance"] = "Moderate"
            st.session_state["optional_notes"] = (
                "The business wants more customers but does not want to weaken brand positioning."
            )

        st.markdown("### 📥 Strategic Simulation Input")

        scenario_input = st.text_area(
            "Describe your business scenario to simulate:",
            key="scenario_input",
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

        if st.session_state["business_stage"] not in stage_options:
            st.session_state["business_stage"] = "Growing"

        if st.session_state["priority_focus"] not in focus_options:
            st.session_state["priority_focus"] = "Revenue Growth"

        if st.session_state["risk_tolerance"] not in risk_options:
            st.session_state["risk_tolerance"] = "Moderate"

        with col1:
            business_stage = st.selectbox(
                "Business Stage",
                stage_options,
                key="business_stage"
            )

            priority_focus = st.selectbox(
                "Priority Focus",
                focus_options,
                key="priority_focus"
            )

        with col2:
            risk_tolerance = st.selectbox(
                "Risk Tolerance",
                risk_options,
                key="risk_tolerance"
            )

        optional_notes = st.text_area(
            "Optional Notes",
            key="optional_notes",
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
                                    "content": (
                                        "You are Rain Intelligence in strategic simulation mode: sharp, executive, "
                                        "realistic, and commercially intelligent."
                                    )
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
                                "Mode": "Scenario Simulation",
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

    # -------------------------
    # MODE 2: Slider-Based Strategic Score
    # -------------------------
    elif mode == "Strategic Score Simulation":
        st.markdown("### 📊 Strategic Score Input")
        st.caption("Use this quick model to pressure-test strategy strength using growth, retention, and margin indicators.")

        market_growth = st.slider("Expected Market Growth (%)", -20, 100, 10)
        customer_retention = st.slider("Customer Retention Rate (%)", 0, 100, 80)
        operating_margin = st.slider("Operating Margin (%)", 0, 100, 25)

        score = (market_growth * 0.4) + (customer_retention * 0.3) + (operating_margin * 0.3)

        st.metric("Strategic Score", f"{score:.2f}")

        if score > 70:
            recommendation = "Aggressive Growth Strategy"
            st.success(f"Recommendation: {recommendation}")
            interpretation = (
                "The indicators suggest strong growth conditions. The business may be positioned to push expansion, "
                "increase visibility, test bigger campaigns, or move more aggressively if capacity can support it."
            )
        elif score > 50:
            recommendation = "Balanced Strategy"
            st.info(f"Recommendation: {recommendation}")
            interpretation = (
                "The indicators suggest a balanced growth posture. The business should continue improving visibility, "
                "retention, and margins while avoiding overextension."
            )
        else:
            recommendation = "Cost Optimization Focus"
            st.warning(f"Recommendation: {recommendation}")
            interpretation = (
                "The indicators suggest caution. The business may need to strengthen margins, retention, or market demand "
                "before pushing aggressive growth."
            )

        summary = f"""
1. Strategic Score Summary
- Expected Market Growth: {market_growth}%
- Customer Retention Rate: {customer_retention}%
- Operating Margin: {operating_margin}%
- Strategic Score: {score:.2f}

2. Recommendation
- {recommendation}

3. Interpretation
- {interpretation}

4. Next Best Actions
- Review whether your market demand is strong enough to support your next move.
- Strengthen retention before scaling if customer loyalty is weak.
- Improve margin before expanding if profitability is too thin.
- Use the AI CMO Engine for deeper growth direction.
- Use Scenario Simulation to pressure-test one specific business decision.

5. Final Simulation Insight
- A strong strategy is not based on excitement alone. It should be supported by market movement, customer stability, and enough margin to survive execution pressure.
"""

        st.subheader("📈 Strategic Score Summary")
        st.markdown(summary)

        st.session_state["strategic_simulator_result"] = summary

        if st.button("💾 Save Strategic Score Result"):
            try:
                save_data("Strategic_Simulator", {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "User_Role": st.session_state.get("user_role", "guest"),
                    "Mode": "Strategic Score Simulation",
                    "Expected_Market_Growth": market_growth,
                    "Customer_Retention": customer_retention,
                    "Operating_Margin": operating_margin,
                    "Strategic_Score": round(score, 2),
                    "Recommendation": recommendation,
                    "Simulation_Result": summary,
                })
                st.success("✅ Strategic score saved.")
            except Exception as save_error:
                st.warning(f"Strategic score generated, but Google Sheets save had an issue: {save_error}")

    # -------------------------
    # PDF Export
    # -------------------------
    if st.session_state.get("strategic_simulator_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer(
            "Strategic Simulation Report",
            st.session_state["strategic_simulator_result"]
        )

        st.download_button(
            "📄 Download Strategic Simulation Report as PDF",
            data=pdf_buffer,
            file_name="Strategic_Simulation_Report.pdf"
        )


if __name__ == "__main__":
    run()