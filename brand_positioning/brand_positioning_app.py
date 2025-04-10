def run():
    st.title("🧭 Brand Positioning")

    st.sidebar.header("💡 Consulting Guide")
    st.sidebar.write("**What to enter here:** Describe your business, audience, or brand challenge.")
    st.sidebar.write("**What this tab does:** Helps define brand identity, audience fit, and positioning.")
    st.sidebar.write("**How to use results:** Use insights to refine messaging, values, and market strategy.")

    prompt_label = "Describe your brand, product, or positioning challenge:"
    example_prompt = "Example: How do I position a wellness brand for millennials interested in mental health?"

    user_input = st.text_area(prompt_label, value=example_prompt, key="brand_positioning_input")

    if st.button("Run GPT Analysis", key="brand_positioning_run") and user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a branding consultant."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"❌ GPT Error: {e}")

    try:
        save_data(st.session_state.get("user_role", "guest"), {"input": user_input}, sheet_tab="Brand Positioning")
        st.info("✅ Data saved to Google Sheets.")
    except Exception as e:
        st.warning(f"Google Sheets not connected. Error: {e}")
