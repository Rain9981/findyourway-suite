def run():
    st.title("📈 Business Development")

    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.write("**What to enter here:** Sales tactics, growth goals, outreach plans, or networking ideas.")
    st.sidebar.write("**What this tab does:** Gives strategies for partnerships, outreach, growth.")
    st.sidebar.write("**How to use results:** Execute new outreach, improve conversion, close deals.")

    prompt_label = "Describe your growth or outreach objective:"
    example_prompt = "Example: How can I develop a B2B partnership plan for my software startup?"

    user_input = st.text_area(prompt_label, value=example_prompt, key="business_development_input")

    if st.button("Run GPT Analysis", key="business_development_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a business development expert."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Business Development")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
