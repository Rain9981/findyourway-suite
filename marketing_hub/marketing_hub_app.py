import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📢 Marketing Hub")
    st.markdown("### Get AI-powered marketing suggestions")

    campaign_goal = st.text_area("Marketing Campaign Goal")

    if st.button("Run GPT Marketing Advice"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a digital marketing consultant."},
                    {"role": "user", "content": campaign_goal}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="MarketingHub")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
