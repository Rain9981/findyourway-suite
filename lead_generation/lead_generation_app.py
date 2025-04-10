import streamlit as st

def run():
    st.title("📣 Lead Generation")

    st.sidebar.header("💡 Lead Gen Guide")
    st.sidebar.markdown("""
    - **Purpose:** Generate new lead capture ideas.
    - **What to input:** Your product/service and target audience.
    - **Use this to:** Get lead magnet and outreach suggestions.
    """)

    prompt = st.text_area("What’s your target market or offer?")
    if st.button("Generate Lead Strategy"):
        st.success(f"📈 Try this lead gen idea: {prompt}")

    user_input = st.text_area(prompt_label, value=example_prompt, key="lead_generation_input")
    if st.button("✨ Autofill Suggestion", key="lead_generation_fill"):
        user_input = "Suggest something for lead generation"


    if st.button("Run GPT Analysis", key="lead_generation_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a lead generation expert."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Lead Generation")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
