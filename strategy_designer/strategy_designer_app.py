import streamlit as st

def run():
    st.title("🧠 Strategy Designer")

    st.sidebar.header("💡 Strategy Designer Guide")
    st.sidebar.markdown("""
    - **Purpose:** Help you plan long-term business strategies.
    - **What to input:** A strategic challenge or goal.
    - **Use this to:** Receive AI-backed strategic suggestions.
    """)

    prompt = st.text_area("Enter your strategic challenge:")
    if st.button("Generate Strategic Advice"):
        st.success(f"🧭 Strategic path forward: {prompt}")

    user_input = st.text_area(prompt_label, value=example_prompt, key="strategy_designer_input")
    if st.button("✨ Autofill Suggestion", key="strategy_designer_fill"):
        user_input = "Suggest something for strategy designer"


    if st.button("Run GPT Analysis", key="strategy_designer_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business strategist."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Strategy Designer")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
