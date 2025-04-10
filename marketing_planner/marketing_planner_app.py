import streamlit as st

def run():
    st.title("📅 Marketing Planner")

    st.sidebar.header("💡 Marketing Planner Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Lets you brainstorm and organize marketing ideas and campaigns.
    - **What to input:** A specific campaign type, date range, or target audience.
    - **How to use:** Structure marketing activities across time and channels.
    """)

    st.info("🧠 Tip: Try input like 'Plan a 3-week social media campaign for new product launch.'")
    plan = st.text_area("What do you want to plan?", key="marketing_planner_input")

    if st.button("Suggest Campaign", key="marketing_planner_btn"):
        st.success(f"📋 Suggested Strategy: Tailor content weekly for your audience — {plan}")
