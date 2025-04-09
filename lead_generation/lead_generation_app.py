import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📣 Lead Generation")
    st.markdown("### Create lead generation copy or strategy")

    industry = st.text_input("Industry")
    audience = st.text_input("Target Audience")

    if st.button("Generate Leads Strategy"):
        try:
            prompt = f"Create a lead generation plan for {industry}, targeting {audience}."
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business growth expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="LeadGen")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
