def run():
    st.title("📣 Lead Generation")

    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.write("**What to enter here:** Your target customer and what you're offering.")
    st.sidebar.write("**What this tab does:** Generates lead magnet ideas and messaging.")
    st.sidebar.write("**How to use results:** Use for email copy, ads, landing pages, or sales scripts.")

    prompt_label = "Describe your ideal lead and product:"
    example_prompt = "Example: I sell an online course for freelancers — generate 3 lead magnet ideas."

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
