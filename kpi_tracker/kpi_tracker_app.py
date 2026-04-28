import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_kpi_prompt(business_goal, business_stage, department, current_metrics, target_outcome, tracking_frequency, main_challenge, optional_notes):
    return f"""
Act as Rain Intelligence in KPI and performance measurement mode: analytical, structured, practical, and business-focused.

Return this exact structure:

1. KPI Snapshot
2. Primary Business Goal
3. Recommended KPIs
4. Leading Indicators
5. Lagging Indicators
6. Tracking Frequency
7. Performance Risks
8. Dashboard / Reporting Suggestions
9. FYW Tool Match
10. Next Best Actions
11. Final KPI Insight

Business Goal:
{business_goal}

Business Stage:
{business_stage}

Department / Focus Area:
{department}

Current Metrics:
{current_metrics}

Target Outcome:
{target_outcome}

Tracking Frequency:
{tracking_frequency}

Main Challenge:
{main_challenge}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Growth
- Forecasting
- AI CMO Engine
- Strategic Simulator
- CRM Dashboard
- Marketing Planner
- Lead Generation
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

    st.title("📊 KPI Tracker")
    st.caption("Define, track, and improve the key performance indicators that show whether your strategy is working.")

    st.sidebar.header("💡 KPI Tracker Guide")
    st.sidebar.markdown("""
**What this tool does:**
- recommends KPIs based on your business goal
- separates leading and lagging indicators
- helps decide what to track and how often
- connects measurement to growth strategy

**Best use:**
Use after Growth, Forecasting, Marketing Planner, or AI CMO Engine when you need to measure results.

**Pro Tip:** KPIs should not just look impressive. They should tell you what to improve next.
""")

    defaults = {
        "kpi_business_goal": "",
        "kpi_current_metrics": "",
        "kpi_target_outcome": "",
        "kpi_main_challenge": "",
        "kpi_optional_notes": "",
        "kpi_business_stage": "Growing",
        "kpi_department": "Marketing",
        "kpi_tracking_frequency": "Weekly",
        "kpi_result": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.button("✨ Autofill Suggestion"):
        st.session_state["kpi_business_goal"] = "Increase Elite subscription upgrades and improve lead-to-customer conversion."
        st.session_state["kpi_business_stage"] = "Growing"
        st.session_state["kpi_department"] = "Marketing"
        st.session_state["kpi_current_metrics"] = "Website visits, email clicks, form submissions, booked calls, and subscription upgrades."
        st.session_state["kpi_target_outcome"] = "Create a clear dashboard that shows which marketing actions are creating real conversions."
        st.session_state["kpi_tracking_frequency"] = "Weekly"
        st.session_state["kpi_main_challenge"] = "There are multiple tools and campaigns, but performance is not yet organized into a simple decision dashboard."
        st.session_state["kpi_optional_notes"] = "The KPI setup should support FYW growth, CMO service delivery, and better decision-making."

    st.markdown("### 📥 KPI Input")

    business_goal = st.text_area("Business Goal", key="kpi_business_goal", height=100)
    current_metrics = st.text_area("Current Metrics Being Tracked", key="kpi_current_metrics", height=100)
    target_outcome = st.text_area("Target Outcome", key="kpi_target_outcome", height=100)

    col1, col2, col3 = st.columns(3)

    with col1:
        business_stage = st.selectbox(
            "Business Stage",
            ["Startup", "Growing", "Established", "Scaling"],
            key="kpi_business_stage"
        )

    with col2:
        department = st.selectbox(
            "Focus Area",
            ["Marketing", "Sales", "Operations", "Customer Experience", "Finance", "Growth", "Team Performance"],
            key="kpi_department"
        )

    with col3:
        tracking_frequency = st.selectbox(
            "Tracking Frequency",
            ["Daily", "Weekly", "Biweekly", "Monthly", "Quarterly"],
            key="kpi_tracking_frequency"
        )

    main_challenge = st.text_area("Main Measurement Challenge", key="kpi_main_challenge", height=90)
    optional_notes = st.text_area("Optional Notes", key="kpi_optional_notes", height=90)

    if st.button("🚀 Generate KPI Strategy"):
        required = [business_goal.strip(), target_outcome.strip(), main_challenge.strip()]
        if not all(required):
            st.warning("⚠️ Please complete the main KPI fields before generating.")
        else:
            try:
                with st.spinner("Building KPI strategy..."):
                    prompt = build_kpi_prompt(
                        business_goal,
                        business_stage,
                        department,
                        current_metrics,
                        target_outcome,
                        tracking_frequency,
                        main_challenge,
                        optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are Rain Intelligence in KPI strategy mode: analytical, practical, structured, and measurement-focused."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.75,
                    )

                    output = response.choices[0].message.content
                    st.session_state["kpi_result"] = output

                    try:
                        save_data("KPI_Tracker", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Business_Goal": business_goal,
                            "Business_Stage": business_stage,
                            "Focus_Area": department,
                            "Current_Metrics": current_metrics,
                            "Target_Outcome": target_outcome,
                            "Tracking_Frequency": tracking_frequency,
                            "Main_Challenge": main_challenge,
                            "Optional_Notes": optional_notes,
                            "KPI_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ KPI strategy generated.")
                st.subheader("📊 KPI Strategy Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("kpi_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("KPI Tracker Report", st.session_state["kpi_result"])
        st.download_button("📄 Download KPI Tracker Report", pdf_buffer, file_name="KPI_Tracker_Report.pdf")


if __name__ == "__main__":
    run()