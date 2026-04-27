import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except Exception:
    TEXTBLOB_AVAILABLE = False


def build_sentiment_prompt(
    user_input,
    audience_type,
    communication_type,
    goal,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in communication and sentiment analysis mode: precise, emotionally intelligent, strategic, and practical.

You are not just labeling sentiment.
You are analyzing emotional tone, audience reaction, trust signals, persuasion strength, and communication risk.

Return the response in this exact structure:

1. Sentiment Snapshot
2. Emotional Tone Read
3. Audience Perception Risk
4. Trust and Persuasion Strength
5. What Is Working
6. What Could Be Improved
7. Suggested Rewrite Direction
8. FYW Tool Match
9. Final Communication Insight

Text to Analyze:
{user_input}

Audience Type:
{audience_type}

Communication Type:
{communication_type}

Communication Goal:
{goal}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW tools:
- Marketing Hub
- Email Marketing
- Brand Positioning
- Mastermind Analyzer
- AI CMO Engine
- Strategic Simulator
- Consulting Guide
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

    st.title("💬 Sentiment Analysis")
    st.caption("Analyze communication tone, emotional impact, trust signals, and audience perception before publishing.")

    st.sidebar.header("💡 Sentiment Guide")
    st.sidebar.markdown("""
**What this tool does:**
- analyzes positive, neutral, or negative tone
- reviews emotional impact and audience perception
- helps improve messaging before publishing
- offers both quick sentiment scoring and deeper AI insight

**Sentiment Modes:**
1. **AI Sentiment Insight** — deeper communication strategy.
2. **Quick Sentiment Check** — fast polarity and subjectivity scoring.

**Pro Tip:** Use Quick Sentiment Check for fast reads, and AI Sentiment Insight for important copy, campaigns, or client-facing messages.
""")

    if "sentiment_analysis_input" not in st.session_state:
        st.session_state["sentiment_analysis_input"] = ""

    if "sentiment_optional_notes" not in st.session_state:
        st.session_state["sentiment_optional_notes"] = ""

    if "sentiment_analysis_result" not in st.session_state:
        st.session_state["sentiment_analysis_result"] = ""

    if "sentiment_audience_type" not in st.session_state:
        st.session_state["sentiment_audience_type"] = "Customers"

    if "sentiment_communication_type" not in st.session_state:
        st.session_state["sentiment_communication_type"] = "Customer Feedback"

    if "sentiment_goal" not in st.session_state:
        st.session_state["sentiment_goal"] = "Understand tone and improve communication"

    mode = st.radio(
        "Choose Sentiment Mode",
        ["AI Sentiment Insight", "Quick Sentiment Check"],
        horizontal=True
    )

    if mode == "AI Sentiment Insight":
        if st.button("✨ Suggest Sentiment Example"):
            st.session_state["sentiment_analysis_input"] = (
                "The customer said the service was slow, but they appreciated the staff’s kindness and said they would consider using us again if timing improved."
            )
            st.session_state["sentiment_audience_type"] = "Customers"
            st.session_state["sentiment_communication_type"] = "Customer Feedback"
            st.session_state["sentiment_goal"] = "Understand tone and improve communication"
            st.session_state["sentiment_optional_notes"] = (
                "This feedback came after a delayed service appointment."
            )

        st.markdown("### 📥 Sentiment Input")

        user_input = st.text_area(
            "Enter customer feedback, campaign copy, social post, email, review, or message:",
            key="sentiment_analysis_input",
            height=150,
            placeholder="Paste the message or feedback you want to analyze."
        )

        col1, col2 = st.columns(2)

        audience_options = ["Customers", "Leads", "Clients", "Team Members", "Partners", "Public Audience"]
        communication_options = [
            "Customer Feedback",
            "Review",
            "Sales Copy",
            "Email",
            "Social Media Post",
            "Ad Copy",
            "Website Copy",
            "Internal Message"
        ]

        with col1:
            audience_type = st.selectbox(
                "Audience Type",
                audience_options,
                key="sentiment_audience_type"
            )

            communication_type = st.selectbox(
                "Communication Type",
                communication_options,
                key="sentiment_communication_type"
            )

        with col2:
            goal = st.text_input(
                "Communication Goal",
                key="sentiment_goal"
            )

        optional_notes = st.text_area(
            "Optional Notes",
            key="sentiment_optional_notes",
            height=100,
            placeholder="Add context such as situation, campaign goal, complaint background, or audience sensitivity."
        )

        if st.button("🚀 Analyze with GPT-4o"):
            if not user_input.strip():
                st.warning("⚠️ Please enter text before analyzing.")
            else:
                try:
                    with st.spinner("Analyzing sentiment and communication impact..."):
                        prompt = build_sentiment_prompt(
                            user_input=user_input,
                            audience_type=audience_type,
                            communication_type=communication_type,
                            goal=goal,
                            optional_notes=optional_notes,
                        )

                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are Rain Intelligence in communication analysis mode: emotionally intelligent, "
                                        "strategic, clear, and focused on tone, perception, persuasion, and trust."
                                    )
                                },
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.75,
                        )

                        output = response.choices[0].message.content
                        st.session_state["sentiment_analysis_result"] = output

                        try:
                            save_data("Sentiment_Analysis", {
                                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "User_Role": st.session_state.get("user_role", "guest"),
                                "Mode": "AI Sentiment Insight",
                                "Audience_Type": audience_type,
                                "Communication_Type": communication_type,
                                "Goal": goal,
                                "Input_Text": user_input,
                                "Optional_Notes": optional_notes,
                                "Sentiment_Result": output,
                            })
                        except Exception as save_error:
                            st.warning(f"Sentiment analyzed, but Google Sheets save had an issue: {save_error}")

                    st.success("✅ Sentiment insight generated.")
                    st.subheader("💬 Sentiment Analysis Report")
                    st.markdown(output)

                except Exception as e:
                    st.error(f"❌ GPT Error: {e}")

    elif mode == "Quick Sentiment Check":
        st.markdown("### ⚡ Quick Sentiment Check")

        if not TEXTBLOB_AVAILABLE:
            st.warning("TextBlob is not available in this environment. Add `textblob` to requirements.txt if needed.")
        else:
            quick_input = st.text_area(
                "Enter market news, tweets, customer comments, reviews, or text to analyze:",
                key="quick_sentiment_input",
                height=150
            )

            if quick_input:
                blob = TextBlob(quick_input)
                sentiment = blob.sentiment

                polarity = round(sentiment.polarity, 2)
                subjectivity = round(sentiment.subjectivity, 2)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Polarity", f"{polarity:.2f}")
                with col2:
                    st.metric("Subjectivity", f"{subjectivity:.2f}")

                if sentiment.polarity > 0:
                    label = "Positive"
                    st.success("Positive sentiment")
                elif sentiment.polarity < 0:
                    label = "Negative"
                    st.error("Negative sentiment")
                else:
                    label = "Neutral"
                    st.info("Neutral sentiment")

                output = f"""
1. Quick Sentiment Summary
- Sentiment Label: {label}
- Polarity: {polarity}
- Subjectivity: {subjectivity}

2. Interpretation
- Polarity measures whether the tone leans negative, neutral, or positive.
- Subjectivity measures whether the text sounds opinion-based or more factual.

3. Communication Note
- Use this quick read as a first signal, then use AI Sentiment Insight for deeper messaging strategy.
"""

                st.session_state["sentiment_analysis_result"] = output
                st.markdown(output)

                try:
                    save_data("Sentiment_Analysis", {
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "User_Role": st.session_state.get("user_role", "guest"),
                        "Mode": "Quick Sentiment Check",
                        "Input_Text": quick_input,
                        "Polarity": polarity,
                        "Subjectivity": subjectivity,
                        "Sentiment_Label": label,
                        "Sentiment_Result": output,
                    })
                except Exception as save_error:
                    st.warning(f"Sentiment analyzed, but Google Sheets save had an issue: {save_error}")

    if st.session_state.get("sentiment_analysis_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Sentiment Analysis Report", st.session_state["sentiment_analysis_result"])

        st.download_button(
            "📄 Download Sentiment Analysis Report as PDF",
            data=pdf_buffer,
            file_name="Sentiment_Analysis_Report.pdf"
        )


if __name__ == "__main__":
    run()