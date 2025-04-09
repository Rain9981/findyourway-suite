import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("AI-Enhanced Tool: " + "subscription_plans".replace("_", " ").title())
    st.markdown("### Use GPT-4o to generate insights.")

    user_input = st.text_area("Enter your business question or topic:")

    if st.button("Run GPT Analysis") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a consulting expert. Help the client with insights."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Analysis failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="subscription_plans".replace("_", " ").title())
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")

    if st.button("Export to PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        y = 750
        for k, v in locals().items():
            if not k.startswith("_"):
                c.drawString(100, y, f"{k}: {v}")
                y -= 15
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, file_name="report.pdf")

    # 🧠 Sidebar Consulting Tips
    with st.sidebar:
        st.markdown("## 🧠 Consulting Tips")
        st.markdown("- Enter a clear business scenario.")
        st.markdown("- Results saved to Google Sheets.")
        st.markdown("- Export your insights as a report.")
