import streamlit as st

def run():
    st.title("📢 Marketing Hub")

    st.sidebar.header("💡 Marketing Hub Guide")
    st.sidebar.markdown("""
    - **Purpose:** Centralize all your marketing insights.
    - **What to input:** Describe your marketing mix, campaigns, or customer segments.
    - **Use this to:** Generate outreach strategies and performance enhancements.
    """)

    prompt = st.text_area("Enter your marketing challenge or objective:")
    if st.button("Run GPT Suggestion"):
        st.success(f"🚀 Here's how to boost your marketing: {prompt}")

    user_input = st.text_area(prompt_label, value=example_prompt, key="marketing_hub_input")
    if st.button("✨ Autofill Suggestion", key="marketing_hub_fill"):
        user_input = "Suggest something for marketing hub"


    if st.button("Run GPT Analysis", key="marketing_hub_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a marketing strategist."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Marketing Hub")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
