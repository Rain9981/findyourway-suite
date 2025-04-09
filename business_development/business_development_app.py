import streamlit as st
from openai import OpenAI
from backend.google_sheets import save_data

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def run():
    st.title("📈 Business Development")
    st.markdown("### Develop business opportunities")

    product = st.text_input("Your product or service")
    goal = st.text_input("Growth goal")

    if st.button("Get Strategy"):
        try:
            query = f"Suggest a business development plan for '{product}' to achieve '{goal}'."
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategist."},
                    {"role": "user", "content": query}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT failed: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), locals(), sheet_tab="BizDev")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
