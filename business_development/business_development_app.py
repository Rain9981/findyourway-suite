import streamlit as st
import pandas as pd
import openai


openai.api_key = st.secrets['openai']['api_key']

def run():
    st.title("💼 Business Development")
    st.markdown("### Plan business expansion.")

    dev_goals = st.text_area("Growth Goals")

    if st.button("Run GPT Analysis"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze the following input: "},
                {"role": "user", "content": business_name if 'business_name' in locals() else 'N/A'}
            ]
        )
        st.success(response['choices'][0]['message']['content'].strip())

    # Google Sheets saving (optional backend logic)
    try:
        from backend.google_sheets import save_data
        save_data(st.session_state.get("user_role", "guest"), locals())
        st.info("✅ Data saved to Google Sheets.")
    except:
        st.warning("Google Sheets not connected.")
