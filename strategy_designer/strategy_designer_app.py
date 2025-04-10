def run():
    st.title("🧠 Strategy Designer")

    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.write("**What to enter here:** Business ideas, SWOT details, or high-level goals.")
    st.sidebar.write("**What this tab does:** Helps form strategic plans using AI guidance.")
    st.sidebar.write("**How to use results:** Map your roadmap, eliminate weak areas, move with clarity.")

    prompt_label = "Describe your strategy challenge or idea:"
    example_prompt = "Example: Design a 6-month strategy for entering a new niche market in digital wellness."

    user_input = st.text_area(prompt_label, value=example_prompt, key="strategy_designer_input")

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
