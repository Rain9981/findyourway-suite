import streamlit as st


def run():
    st.title("🌐 Welcome to Find Your Way AI Consulting Suite")

    st.markdown(
        """
        This suite is designed to give you access to strategic business tools based on your membership level.
        Use this homepage to understand your access, know what this suite is connected to, and find your next step.
        For full guidance on how to use the tools in order, visit the **Consulting Guide** tab.
        """
    )

    st.sidebar.header("🧭 Homepage Tips")
    st.sidebar.markdown(
        """
        - Use this page for orientation and quick access.
        - Visit **Consulting Guide** if you need walkthrough help.
        - Your visible tools are based on your current access tier.
        - Upgrade through FYW InterNetwork to unlock more.
        """
    )

    role = st.session_state.get("user_role", "guest")

    if role == "admin":
        greeting = "Welcome, Admin! You have full suite access, including backend and user management tools."
    elif role == "premium":
        greeting = "Welcome, Premium Member! You have advanced execution, planning, and communication tools available."
    elif role == "elite":
        greeting = "Welcome, Elite Member! You have expanded strategy, growth, and marketing support tools."
    elif role == "basic":
        greeting = "Welcome, Basic Member! You have access to the core foundation tools to begin your journey."
    else:
        greeting = "Welcome! Please log in to access your consulting tools."

    st.subheader(greeting)

    st.image(
        "https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif",
        width=400,
        caption="Find Your Way Forward ✨"
    )

    st.divider()

    st.markdown("## 🔗 Connected to FYW InterNetwork")
    st.markdown(
        """
        Your access to this consulting suite is connected to the **Find Your Way InterNetwork**.
        As your membership level increases, your available tools and consulting depth increase with it.
        """
    )

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

    st.markdown("## 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📘 Open Consulting Guide"):
            st.info("Go to the 'Consulting Guide' tab for full walkthrough guidance and recommended tool flow.")

    with col2:
        st.markdown(
            """
            **Need more access?**  
            [Upgrade Membership](https://findyourwaynmc.com/internetwork#internetwork-membership)
            """
        )

    with col3:
        st.markdown(
            """
            **Visit FYW Website**  
            [Go to FindYourWayNMC.com](https://findyourwaynmc.com)
            """
        )

    st.divider()

    st.markdown("## 🧠 Need Guidance?")
    st.markdown(
        """
        If you are unsure which tool to use next, go to the **Consulting Guide** tab.
        That guide explains the tool order, what each tab is for, and which FYW programs or services pair best with each one.
        """
    )

    st.markdown("## 📌 Important Note")
    st.markdown(
        """
        Some tools are intentionally hidden based on your current access level.
        If you do not see certain tools, that usually means they are part of a higher membership tier or admin-only workflow.
        """
    )