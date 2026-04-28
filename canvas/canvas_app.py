import streamlit as st
import io
import datetime
from openai import OpenAI
from backend.google_sheets import save_data
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter


def build_canvas_prompt(user_input):
    return f"""
Act as Rain Intelligence in rapid business concept analysis mode.

Turn this idea into a structured business canvas.

Return this exact format:

1. Business Snapshot
2. Value Proposition
3. Target Customers
4. Problem Being Solved
5. Revenue Streams
6. Channels
7. Key Activities
8. Key Resources
9. Key Partners
10. Cost Structure
11. Strength of Idea
12. Weakness or Risk
13. Next Steps
14. Final Insight

Business Idea:
{user_input}
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

    st.title("🧩 Canvas Builder")
    st.caption("Quickly turn a business idea into a structured business canvas.")

    st.sidebar.header("💡 Canvas Builder Guide")
    st.sidebar.markdown("""
**What this tool does:**
- turns a raw idea into a business model canvas
- helps you think through structure quickly
- highlights strengths and risks

**Best use:**
Use BEFORE Business Model Canvas when the idea is still forming.

**Pro Tip:** This is for speed. Use the full Canvas tab when you need precision.
""")

    if "canvas_input_v2" not in st.session_state:
        st.session_state["canvas_input_v2"] = ""

    if "canvas_result_v2" not in st.session_state:
        st.session_state["canvas_result_v2"] = ""

    if st.button("✨ Autofill Example"):
        st.session_state["canvas_input_v2"] = (
            "I want to start a mobile car detailing business targeting busy professionals in urban areas "
            "who want convenience and premium service."
        )

    user_input = st.text_area(
        "Describe your business idea:",
        key="canvas_input_v2",
        height=150
    )

    if st.button("🚀 Generate Canvas"):
        if not user_input.strip():
            st.warning("⚠️ Please enter your business idea.")
        else:
            try:
                with st.spinner("Building canvas..."):
                    prompt = build_canvas_prompt(user_input)

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are Rain Intelligence in business concept mode: clear, strategic, and practical."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                    )

                    output = response.choices[0].message.content
                    st.session_state["canvas_result_v2"] = output

                    try:
                        save_data("Canvas_Quick", {
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User_Role": st.session_state.get("user_role", "guest"),
                            "Idea": user_input,
                            "Canvas_Result": output,
                        })
                    except Exception as save_error:
                        st.warning(f"Saved locally, but Sheets error: {save_error}")

                st.success("✅ Canvas generated.")
                st.subheader("🧩 Canvas Output")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ GPT Error: {e}")

    if st.session_state.get("canvas_result_v2"):
        st.divider()
        pdf_buffer = create_pdf_buffer("Canvas Builder Report", st.session_state["canvas_result_v2"])

        st.download_button(
            "📄 Download Canvas Report",
            pdf_buffer,
            file_name="Canvas_Builder_Report.pdf"
        )


if __name__ == "__main__":
    run()