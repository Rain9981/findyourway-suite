import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🤝 Network Builder")
    st.markdown("### Build strategic relationships and expand your influence.")

    st.sidebar.header("💡 Network Builder Guide")
    st.sidebar.write("**What this tab does:** Helps brainstorm ways to grow your personal or business network.")
    st.sidebar.write("**What to enter:** Describe the industry, people, or purpose of the networking effort.")
    st.sidebar.write("**How to use:** Use GPT to generate connection strategies, event ideas, or outreach messages.")

    example_prompt = "How can I build connections with real estate investors in Atlanta?"
    user_input = st.text_area("Who are you trying to connect with or influence?", value=example_prompt, key="network_builder_input")

    if st.button("Autofill Network Strategy", key="network_builder_autofill") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a networking strategist helping users build valuable connections."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(
            st.session_state.get("user_role", "guest"),
            {"input": user_input},
            sheet_tab="Network Builder"
        )
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="network_builder_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Network Builder Report")
        c.drawString(100, 735, f"Input: {user_input}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_builder_report.pdf")
        except Exception as e:
            st.error(f"GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": prompt}, sheet_tab="network builder")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF", key="network_builder_pdf"):
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "GPT Analysis for network builder")
        c.drawString(100, 735, f"Prompt: {prompt}")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="network_builder_report.pdf")
