def run():
    st.title("📢 Marketing Hub")

    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.write("**What to enter here:** Your campaign idea or marketing objective.")
    st.sidebar.write("**What this tab does:** Plans multi-channel campaigns using AI logic.")
    st.sidebar.write("**How to use results:** Guide content creation, ad targeting, and launch plans.")

    prompt_label = "Describe your marketing campaign or audience:"
    example_prompt = "Example: Plan a cross-platform launch for a productivity app targeting Gen Z entrepreneurs."

    user_input = st.text_area(prompt_label, value=example_prompt, key="marketing_hub_input")

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
