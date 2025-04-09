import streamlit as st
from openai import OpenAI
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from backend.google_sheets import save_data

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("🧭 Brand Positioning")
    st.markdown("### Define your unique market identity")

    brand_description = st.text_area("Describe your brand")
    
    if st.button("Analyze Brand"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a brand strategist."},
                    {"role": "user", "content": brand_description}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="BrandPositioning")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
