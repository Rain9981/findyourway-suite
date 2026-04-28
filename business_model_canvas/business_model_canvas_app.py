import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_canvas_prompt(
    business_name,
    value_proposition,
    customer_segments,
    revenue_streams,
    channels,
    key_activities,
    key_resources,
    partners,
    cost_structure,
    optional_notes,
):
    return f"""
Act as Rain Intelligence in business architecture mode.

Build a professional Business Model Canvas using structured clarity.

Return in this format:

1. Business Snapshot
2. Value Proposition
3. Customer Segments
4. Revenue Streams
5. Channels
6. Key Activities
7. Key Resources
8. Key Partners
9. Cost Structure
10. Strategic Strength
11. Weak Points
12. Next Actions

Business Name: {business_name}
Value Proposition: {value_proposition}
Customer Segments: {customer_segments}
Revenue Streams: {revenue_streams}
Channels: {channels}
Key Activities: {key_activities}
Key Resources: {key_resources}
Partners: {partners}
Cost Structure: {cost_structure}
Notes: {optional_notes}
"""


def run():
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.title("🧩 Business Model Canvas V2")
    st.caption("Build a structured business model with strategic clarity.")

    if "canvas_result" not in st.session_state:
        st.session_state["canvas_result"] = ""

    if st.button("✨ Autofill Example"):
        st.session_state.update({
            "canvas_name": "Mobile Car Detailing",
            "canvas_value": "Convenient premium car care at customer location",
            "canvas_customers": "Busy professionals",
            "canvas_revenue": "Service packages",
            "canvas_channels": "Website, referrals",
            "canvas_activities": "Cleaning, booking",
            "canvas_resources": "Equipment, labor",
            "canvas_partners": "Suppliers",
            "canvas_costs": "Labor, supplies",
            "canvas_notes": "Urban market"
        })

    st.markdown("### 📥 Canvas Inputs")

    business_name = st.text_input("Business Name", key="canvas_name")
    value_proposition = st.text_area("Value Proposition", key="canvas_value")
    customer_segments = st.text_area("Customer Segments", key="canvas_customers")
    revenue_streams = st.text_area("Revenue Streams", key="canvas_revenue")
    channels = st.text_area("Channels", key="canvas_channels")
    key_activities = st.text_area("Key Activities", key="canvas_activities")
    key_resources = st.text_area("Key Resources", key="canvas_resources")
    partners = st.text_area("Key Partners", key="canvas_partners")
    cost_structure = st.text_area("Cost Structure", key="canvas_costs")
    optional_notes = st.text_area("Notes", key="canvas_notes")

    if st.button("🚀 Generate Canvas"):
        prompt = build_canvas_prompt(
            business_name,
            value_proposition,
            customer_segments,
            revenue_streams,
            channels,
            key_activities,
            key_resources,
            partners,
            cost_structure,
            optional_notes,
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content
        st.session_state["canvas_result"] = output

        save_data("Canvas", {"Result": output})

        st.success(output)