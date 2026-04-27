import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_network_prompt(
    networking_goal,
    target_connections,
    offer_value,
    current_network,
    connection_type,
    outreach_channel,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in strategic network-building mode: relationship-focused, commercially sharp, clear, and practical.

You are helping the user build strategic relationships, partnerships, referrals, and collaboration opportunities.

Return the response in this exact structure:

1. Network Goal Snapshot
2. Best Connection Targets
3. Relationship Positioning
4. Outreach Strategy
5. Conversation Starters
6. Partnership Opportunities
7. Follow-Up Plan
8. FYW InterNetwork Match
9. Next Best Actions
10. Final Network Insight

Networking Goal:
{networking_goal}

Target Connections:
{target_connections}

Value the User Can Offer:
{offer_value}

Current Network:
{current_network}

Connection Type:
{connection_type}

Preferred Outreach Channel:
{outreach_channel}

Optional Notes:
{optional_notes if optional_notes.strip() else "None provided"}

Relevant FYW ecosystem:
- InterNetwork
- Network Builder
- Lead Generation
- Marketing Hub
- Email Marketing
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

    st.title("🌐 Network Builder")
    st.caption("Build strategic relationships, referral channels, partnerships, and InterNetwork growth opportunities.")

    st.sidebar.header("💡 Network Builder Guide")
    st.sidebar.markdown("""
**What this tool does:**
- helps identify who you should connect with
- creates outreach and follow-up strategy
- supports partnerships, referrals, and collaborations
- connects networking to FYW InterNetwork growth

**Pro Tip:** Strong networking is not just meeting people — it is building aligned relationships with a clear value exchange.
""")

    defaults = {
        "networking_goal": "",
        "target_connections": "",
        "offer_value": "",
        "current_network": "",
        "optional_notes": "",
        "connection_type": "Referral Partnerships",
        "outreach_channel": "Email / Direct Message",
        "network_builder_result": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.button("✨ Autofill Suggestion"):
        st.session_state["networking_goal"] = (
            "I want to build referral partnerships and strategic relationships that can help my business gain more visibility, "
            "more qualified leads, and more collaboration opportunities."
        )
        st.session_state["target_connections"] = (
            "Local business owners, marketing professionals, real estate professionals, coaches, consultants, and service providers."
        )
        st.session_state["offer_value"] = (
            "I can offer design support, business strategy, shared promotion, referrals, and collaboration through the Find Your Way ecosystem."
        )
        st.session_state["current_network"] = (
            "I have some business contacts, but I do not have a structured outreach or follow-up system yet."
        )
        st.session_state["connection_type"] = "Referral Partnerships"
        st.session_state["outreach_channel"] = "Email / Direct Message"
        st.session_state["optional_notes"] = (
            "I want the outreach to feel professional, warm, and strategic without sounding desperate or overly sales-driven."
        )

    st.markdown("### 📥 Network Strategy Input")

    networking_goal = st.text_area(
        "What is your networking goal?",
        key="networking_goal",
        height=120,
        placeholder="Example: I want referral partners, local business connections, affiliates, or collaboration opportunities."
    )

    col1, col2 = st.columns(2)

    with col1:
        connection_type = st.selectbox(
            "Connection Type",
            [
                "Referral Partnerships",
                "Strategic Collaborations",
                "Affiliate Relationships",
                "Local Business Connections",
                "Mentorship / Expert Access",
                "Client Acquisition",
                "Community / Network Growth"
            ],
            key="connection_type"
        )

    with col2:
        outreach_channel = st.selectbox(
            "Preferred Outreach Channel",
            [
                "Email / Direct Message",
                "Social Media",
                "In-Person Networking",
                "Phone Call",
                "LinkedIn",
                "Community Events",
                "Mixed Outreach"
            ],
            key="outreach_channel"
        )

    target_connections = st.text_area(
        "Who are you trying to connect with?",
        key="target_connections",
        height=100,
        placeholder="Example: business owners, marketers, property managers, coaches, local service providers, etc."
    )

    offer_value = st.text_area(
        "What value can you offer them?",
        key="offer_value",
        height=100,
        placeholder="Example: referrals, design support, shared marketing, business strategy, audience access, etc."
    )

    current_network = st.text_area(
        "Describe your current network or relationship base:",
        key="current_network",
        height=100,
        placeholder="Example: I know a few business owners but have no consistent follow-up system."
    )

    optional_notes = st.text_area(
        "Optional Notes",
        key="optional_notes",
        height=100,
        placeholder="Add context about location, industry, audience, confidence level, or relationship goals."
    )

    if st.button("🚀 Generate Network Strategy"):
        required = [
            networking_goal.strip(),
            target_connections.strip(),
            offer_value.strip(),
            current_network.strip(),
        ]

        if not all(required):
            st.warning("⚠️ Please complete the main networking fields before generating.")
        else:
            try:
                with st.spinner("Building your network strategy..."):
                    prompt = build_network_prompt(
                        networking_goal=networking_goal,
                        target_connections=target_connections,
                        offer_value=offer_value,
                        current_network=current_network,
                        connection_type=connection_type,
                        outreach_channel=outreach_channel,
                        optional_notes=optional_notes,
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are Rain Intelligence in network-building mode: strategic, relationship-focused, "
                                    "clear, commercially aware, and action-oriented."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["network_builder_result"] = output

                    try:
                        save_data("Network_Builder", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Networking_Goal": networking_goal,
                            "Connection_Type": connection_type,
                            "Outreach_Channel": outreach_channel,
                            "Target_Connections": target_connections,
                            "Offer_Value": offer_value,
                            "Current_Network": current_network,
                            "Optional_Notes": optional_notes,
                            "GPT_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Strategy generated, but Google Sheets save had an issue: {save_error}")

                st.success("✅ Network strategy generated.")
                st.subheader("🌐 Network Strategy Report")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("network_builder_result"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Network Builder Report", st.session_state["network_builder_result"])

        st.download_button(
            "📄 Download Network Builder Report as PDF",
            data=pdf_buffer,
            file_name="Network_Builder_Report.pdf"
        )


if __name__ == "__main__":
    run()