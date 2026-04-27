import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

try:
    import pandas as pd
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except Exception:
    PROPHET_AVAILABLE = False


def build_forecasting_prompt(
    forecast_input,
    business_stage,
    forecast_focus,
    time_horizon,
    confidence_level,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in business forecasting mode: analytical, strategic, realistic, and commercially useful.

You are not a generic trend writer.
You are a business forecasting strategist helping interpret future expectations, risks, opportunities, and planning moves.

Return the response in this exact structure:

1. Forecast Snapshot
2. Key Assumptions
3. Growth Opportunities
4. Risk Factors
5. Most Likely Outcome
6. Strategic Forecast Interpretation
7. Recommended Next Moves
8. FYW Tool Match
9. Final Forecast Insight

Forecast Input:
{forecast_input}

Business Stage:
{business_stage}

Forecast Focus:
{forecast_focus}

Time Horizon:
{time_horizon}

Confidence Level:
{confidence_level}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- AI CMO Engine
- Strategic Simulator
- Growth
- KPI Tracker
- Forecasting
- Business Development
- Marketing Hub
- Lead Generation
- CRM Dashboard
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

    st.title("📈 Business Forecasting")
    st.caption("Forecast business trends, growth expectations, revenue movement, and future planning direction.")

    st.sidebar.header("💡 Forecasting Guide")
    st.sidebar.markdown("""
**What this tool does:**
- creates AI-based business forecast insight
- interprets future expectations and planning risks
- supports CSV-based forecasting when structured data is available
- helps connect projections to strategy

**Forecasting Modes:**
1. **AI Forecast Guidance** — describe your forecast and receive strategic interpretation.
2. **CSV Forecast Upload** — upload data with `ds` and `y` columns for a 90-day projection.

**Pro Tip:** Use AI Forecast Guidance for strategy. Use CSV Forecast Upload when you have actual historical numbers.
""")

    if "forecasting_input" not in st.session_state:
        st.session_state["forecasting_input"] = ""

    if "forecasting_optional_notes" not in st.session_state:
        st.session_state["forecasting_optional_notes"] = ""

    if "forecasting_result" not in st.session_state:
        st.session_state["forecasting_result"] = ""

    if "forecast_business_stage" not in st.session_state:
        st.session_state["forecast_business_stage"] = "Growing"

    if "forecast_focus" not in st.session_state:
        st.session_state["forecast_focus"] = "Revenue Growth"

    if "forecast_time_horizon" not in st.session_state:
        st.session_state["forecast_time_horizon"] = "Next 90 days"

    if "forecast_confidence" not in st.session_state:
        st.session_state["forecast_confidence"] = "Moderate confidence"

    mode = st.radio(
        "Choose Forecasting Mode",
        ["AI Forecast Guidance", "CSV Forecast Upload"],
        horizontal=True
    )

    if mode == "AI Forecast Guidance":
        if st.button("✨ Suggest Forecast Example"):
            st.session_state["forecasting_input"] = (
                "We expect revenue to increase by 15% over the next quarter due to stronger seasonal demand, "
                "more consistent promotions, and a planned local marketing push."
            )
            st.session_state["forecast_business_stage"] = "Growing"
            st.session_state["forecast_focus"] = "Revenue Growth"
            st.session_state["forecast_time_horizon"] = "Next 90 days"
            st.session_state["forecast_confidence"] = "Moderate confidence"
            st.session_state["forecasting_optional_notes"] = (
                "The business has some momentum, but lead flow and follow-up still need structure."
            )

        st.markdown("### 📥 Forecast Input")

        forecasting_input = st.text_area(
            "Describe your forecast, projection, or future growth expectation:",
            key="forecasting_input",
            height=150,
            placeholder="Example: We expect sales to grow 20% next quarter because of new campaigns, stronger referrals, and improved follow-up."
        )

        col1, col2 = st.columns(2)

        stage_options = ["Idea Stage", "Startup", "Growing", "Established", "Scaling"]
        focus_options = [
            "Revenue Growth",
            "Lead Growth",
            "Customer Retention",
            "Market Demand",
            "Operational Capacity",
            "Profit Margin",
            "Marketing Performance"
        ]
        horizon_options = ["Next 30 days", "Next 90 days", "Next 6 months", "Next 12 months"]
        confidence_options = ["Low confidence", "Moderate confidence", "High confidence"]

        with col1:
            business_stage = st.selectbox(
                "Business Stage",
                stage_options,
                key="forecast_business_stage"
            )

            forecast_focus = st.selectbox(
                "Forecast Focus",
                focus_options,
                key="forecast_focus"
            )

        with col2:
            time_horizon = st.selectbox(
                "Time Horizon",
                horizon_options,
                key="forecast_time_horizon"
            )

            confidence_level = st.selectbox(
                "Confidence Level",
                confidence_options,
                key="forecast_confidence"
            )

        optional_notes = st.text_area(
            "Optional Notes",
            key="forecasting_optional_notes",
            height=100,
            placeholder="Add any important details about budget, staffing, demand, seasonality, competition, or current performance."
        )

        if st.button("🚀 Run Forecast Analysis"):
            if not forecasting_input.strip():
                st.warning("⚠️ Please enter your forecast details before generating.")
            else:
                try:
                    with st.spinner("Generating business forecast insight..."):
                        prompt = build_forecasting_prompt(
                            forecast_input=forecasting_input,
                            business_stage=business_stage,
                            forecast_focus=forecast_focus,
                            time_horizon=time_horizon,
                            confidence_level=confidence_level,
                            optional_notes=optional_notes,
                        )

                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are Rain Intelligence in business forecasting mode: analytical, realistic, strategic, and execution-focused."
                                },
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.75,
                        )

                        output = response.choices[0].message.content
                        st.session_state["forecasting_result"] = output

                        try:
                            save_data("Forecasting", {
                                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "User_Role": st.session_state.get("user_role", "guest"),
                                "Mode": "AI Forecast Guidance",
                                "Forecast_Input": forecasting_input,
                                "Business_Stage": business_stage,
                                "Forecast_Focus": forecast_focus,
                                "Time_Horizon": time_horizon,
                                "Confidence_Level": confidence_level,
                                "Optional_Notes": optional_notes,
                                "AI_Result": output,
                            })
                        except Exception as save_error:
                            st.warning(f"Forecast generated, but Google Sheets save had an issue: {save_error}")

                    st.success("✅ Forecast analysis generated.")
                    st.subheader("📈 Forecasting Report")
                    st.markdown(output)

                except Exception as e:
                    st.error(f"❌ GPT Error: {e}")

    elif mode == "CSV Forecast Upload":
        st.markdown("### 📊 CSV Forecast Upload")
        st.caption("Upload a CSV with two columns: `ds` for date and `y` for the value you want to forecast.")

        if not PROPHET_AVAILABLE:
            st.warning("Prophet or pandas is not available in this environment. Add `prophet` and `pandas` to requirements.txt if needed.")
        else:
            uploaded_file = st.file_uploader("Upload CSV with 'ds' and 'y' columns", key="forecast_csv")

            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)

                    if "ds" not in df.columns or "y" not in df.columns:
                        st.error("CSV must include columns named `ds` and `y`.")
                    else:
                        st.write("Data preview:", df.head())

                        model = Prophet()
                        model.fit(df)

                        future = model.make_future_dataframe(periods=90)
                        forecast = model.predict(future)

                        st.subheader("Forecast Plot")
                        st.line_chart(forecast[["ds", "yhat"]].set_index("ds"))

                        latest_prediction = forecast[["ds", "yhat"]].tail(1)
                        predicted_value = float(latest_prediction["yhat"].iloc[0])

                        output = f"""
1. CSV Forecast Summary
- Rows Processed: {len(df)}
- Forecast Period: 90 days
- Final Projected Value: {predicted_value:.2f}

2. Interpretation
- This forecast uses historical values to estimate future movement.
- Use this as a directional planning tool, not a guaranteed financial outcome.

3. Next Best Actions
- Compare this forecast against your marketing calendar.
- Review whether staffing and operations can support projected growth.
- Use AI CMO Engine to turn the forecast into a growth strategy.
- Use Strategic Simulator to test decisions before acting.
"""

                        st.session_state["forecasting_result"] = output
                        st.markdown(output)

                        try:
                            save_data("Forecasting", {
                                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "User_Role": st.session_state.get("user_role", "guest"),
                                "Mode": "CSV Forecast Upload",
                                "Rows_Processed": len(df),
                                "Forecast_Period_Days": 90,
                                "Final_Projected_Value": round(predicted_value, 2),
                                "AI_Result": output,
                            })
                        except Exception as save_error:
                            st.warning(f"Forecast generated, but Google Sheets save had an issue: {save_error}")

                except Exception as e:
                    st.error(f"Forecasting error: {e}")

    if st.session_state.get("forecasting_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Business Forecasting Report", st.session_state["forecasting_result"])

        st.download_button(
            "📄 Download Forecasting Report as PDF",
            data=pdf_buffer,
            file_name="Business_Forecasting_Report.pdf"
        )


if __name__ == "__main__":
    run()