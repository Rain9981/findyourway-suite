import streamlit as st


def run():
    st.title("🌐 Find Your Way AI Consulting Suite")

    st.markdown("""
    This is not just a tool suite.

    This is a **structured AI consulting system** designed to:
    - build your business correctly
    - create strategy with precision
    - generate leads and clients
    - track and improve performance

    👉 Every tab plays a role in your growth system.
    """)

    st.sidebar.header("🧭 Homepage Tips")
    st.sidebar.markdown("""
    - Start with **Client Intake** if you are unsure
    - Use **Consulting Guide** for full walkthrough help
    - Follow the system flow for best results
    - Your visible tools are based on your access tier
    - Upgrade through FYW InterNetwork to unlock more
    """)

    role = st.session_state.get("user_role", "guest")

    if role == "admin":
        greeting = "Welcome, Admin. Full system access enabled."
    elif role == "premium":
        greeting = "Welcome, Premium Member. Advanced execution tools unlocked."
    elif role == "elite":
        greeting = "Welcome, Elite Member. Strategy and growth tools ready."
    elif role == "basic":
        greeting = "Welcome, Basic Member. Foundation tools available."
    else:
        greeting = "Welcome. Please log in to access your consulting tools."

    st.subheader(greeting)

    st.image(
        "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif",
        width=500,
        caption="Build. Think. Execute. 🚀"
    )

    st.divider()

    st.markdown("## 🚀 Start Here")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Start Client Intake"):
            st.info("Go to the **Client Intake** tab to begin your journey.")

    with col2:
        if st.button("🧠 Find Your Direction"):
            st.info("Go to **Find Where You Win** to discover your strongest path.")

    with col3:
        if st.button("📘 Open Consulting Guide"):
            st.info("Go to the **Consulting Guide** tab for the full walkthrough.")

    st.divider()

    st.markdown("## 🧭 Choose Your Path")
    st.markdown("""
    - **New or unsure?** → Start with **Client Intake**
    - **Need direction?** → Use **Find Where You Win**
    - **Have an idea?** → Use **Canvas** or **Business Model Canvas**
    - **Need growth?** → Use **Growth** or **AI CMO Engine**
    - **Have clients?** → Go to **CRM Manager**
    """)

    st.divider()

    st.markdown("## ⚡ Quick Actions")

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("📈 Build Growth Strategy"):
            st.info("Open the **Growth** tab.")

    with col5:
        if st.button("🧠 Run AI CMO Engine"):
            st.info("Open the **AI CMO Engine** tab.")

    with col6:
        if st.button("🧾 Manage Clients"):
            st.info("Open the **CRM Manager** tab.")

    st.divider()

    st.markdown("## 🔄 How the System Works")
    st.markdown("""
    **Client Intake → Direction → Business Structure → Strategy → Marketing → CRM → Growth → KPI Tracking**

    This flow helps you move from idea or confusion into structure, execution, and measurable progress.
    """)

    st.divider()

    st.markdown("## 🔗 Connected to FYW InterNetwork")
    st.markdown("""
    Your access to this consulting suite is connected to the **Find Your Way InterNetwork**.

    As your membership level increases, your available tools and consulting depth increase with it.
    """)

    st.markdown("## 🎯 Your Current Access")

    if role == "basic":
        st.info(
            "You currently have foundation-level access. This is ideal for clarity, positioning, and early planning."
        )
    elif role == "elite":
        st.info(
            "You currently have expanded access for strategy, marketing direction, and growth-focused planning."
        )
    elif role == "premium":
        st.info(
            "You currently have advanced access for execution, communication tools, and deeper consulting support."
        )
    elif role == "admin":
        st.success(
            "You currently have full internal access across the suite, including CRM and admin management tools."
        )
    else:
        st.warning("Log in to view your current suite access level.")

    st.divider()

    st.markdown("## 🔗 Helpful Links")

    col7, col8 = st.columns(2)

    with col7:
        st.markdown("""
        **Need more access?**  
        [Upgrade Membership](https://findyourwaynmc.com/internetwork#internetwork-membership)
        """)

    with col8:
        st.markdown("""
        **Visit FYW Website**  
        [Go to FindYourWayNMC.com](https://findyourwaynmc.com)
        """)

    st.divider()

    st.markdown("## 📌 Important Note")
    st.markdown("""
    Some tools are intentionally hidden based on your current access level.
    If you do not see certain tools, that usually means they are part of a higher membership tier or admin-only workflow.
    """)


if __name__ == "__main__":
    run()