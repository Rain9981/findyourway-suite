import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_crm_prompt(client_name, notes, stage, goal, urgency, optional_notes):
    return f"""
Act as Rain Intelligence in CRM intelligence mode.

Analyze this client interaction and return:

1. Client Snapshot
2. Client Intent Level (Hot / Warm / Cold)
3. Key Concerns or Objections
4. Opportunity Level
5. Risk of Losing Client
6. Recommended Next Move
7. Suggested Message to Send
8. Follow-Up Strategy
9. Revenue Potential
10. FYW Tool Match
11. Final Insight

Client Name:
{client_name}

Client Stage:
{stage}

Session Notes:
{notes}

Goal:
{goal}

Urgency:
{urgency}

Additional Context:
{optional_notes if optional_notes.strip() else "None"}
"""


def create_pdf(title, client_name, notes, output):
    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=letter)

    c.drawString(100, 750, title)
    c.drawString(100, 730, f"Client: {client_name}")

    text = c.beginText(100, 710)
    for line in notes.split("\n"):
        text.textLine(line[:100])
    c.drawText(text)

    insight_text = c.beginText(100, 600)
    for line in output.split("\n"):
        insight_text.textLine(line[:100])
    c.drawText(insight_text)

    c.save()
    buffer.seek(0)
    return buffer


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🧠 CRM Intelligence Engine")
    st.caption("Analyze client interactions and turn them into strategic actions and revenue opportunities.")

    st.sidebar.header("💡 CRM Intelligence Guide")
    st.sidebar.markdown("""
**What this tool does:**
- analyzes client conversations
- detects intent, objections, and opportunities
- recommends next actions
- improves conversion and retention

**Pro Tip:** Every client note is data. This turns that data into decisions.
""")

    if "crm_result" not in st.session_state:
        st.session_state["crm_result"] = ""

    if st.button("✨ Autofill Example"):
        st.session_state["crm_name"] = "John Smith"
        st.session_state["crm_notes"] = "Client likes the service but hesitant about pricing and commitment."
        st.session_state["crm_stage"] = "Lead"
        st.session_state["crm_goal"] = "Convert to paying client"
        st.session_state["crm_urgency"] = "Moderate"
        st.session_state["crm_optional"] = "Wants flexibility"

    client_name = st.text_input("Client Name", key="crm_name")
    notes = st.text_area("Session Notes", key="crm_notes", height=120)

    col1, col2 = st.columns(2)

    with col1:
        stage = st.selectbox("Client Stage", ["Lead", "Active", "Inactive"], key="crm_stage")

    with col2:
        urgency = st.selectbox("Urgency", ["Low", "Moderate", "High"], key="crm_urgency")

    goal = st.text_area("Goal with this client", key="crm_goal")
    optional_notes = st.text_area("Optional Notes", key="crm_optional")

    if st.button("🚀 Analyze Client"):
        if not notes.strip():
            st.warning("Enter notes first.")
        else:
            with st.spinner("Analyzing client..."):
                prompt = build_crm_prompt(client_name, notes, stage, goal, urgency, optional_notes)

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are Rain Intelligence in CRM strategy mode."},
                        {"role": "user", "content": prompt}
                    ]
                )

                output = response.choices[0].message.content
                st.session_state["crm_result"] = output

                save_data("CRM_Insights_V2", {
                    "Client": client_name,
                    "Notes": notes,
                    "Result": output
                })

                st.success(output)

    if st.session_state["crm_result"]:
        pdf = create_pdf("CRM Report", client_name, notes, st.session_state["crm_result"])
        st.download_button("📄 Download Report", pdf, file_name="crm_report.pdf")


if __name__ == "__main__":
    run()