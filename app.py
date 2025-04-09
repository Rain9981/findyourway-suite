import streamlit as st
import importlib
import os

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌍 Branding with businessman spinner + logo
st.markdown("""
<div style='text-align:center;'>
    <h1>🌍 Find Your Way Network Marketing Consultants</h1>
    <img src='https://i.gifer.com/VAyR.gif' width='100' style='margin-top:10px;'>
    <br/>
    <img src='https://findyourwaynmc.wixsite.com/my-site/_files/ugd/2bd6a2_0a1d305fc8e24ab5b9e26ea5e8f15f60~mv2.png' width='140' style='margin-top:5px;'>
</div>
""", unsafe_allow_html=True)

# 🔐 Login with tier access
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = "guest"

if not st.session_state.logged_in:
    st.subheader("🔐 Login Required")
    password = st.text_input("Enter access password:", type="password")

    roles = {
        "basic": "basic",
        "elite": "elite",
        "premium": "premium",
        "FindYourWayNMC520": "admin"
    }

    if st.button("Login"):
        if password in roles:
            st.session_state.logged_in = True
            st.session_state.user_role = roles[password]
            st.success(f"✅ Logged in as {st.session_state.user_role.capitalize()}")
            st.rerun()  # ✅ Safe for Streamlit Cloud
        else:
            st.error("❌ Incorrect password")
    st.stop()

# 🔍 Sidebar dropdown navigation
st.sidebar.title("📂 Choose a Tool")
tabs = sorted([f for f in os.listdir() if os.path.isdir(f) and not f.startswith(".") and os.path.exists(f"{f}/{f}_app.py")])
selected_tab = st.sidebar.selectbox("Select Tab", tabs)

# 📘 Sidebar guide per tab (load from file if exists)
guide_path = f"guides/{selected_tab}_guide.txt"
if os.path.exists(guide_path):
    with open(guide_path, "r") as f:
        st.sidebar.markdown("💡 Guide")
        st.sidebar.info(f.read())

# 🚀 Run selected module
module = importlib.import_module(f"{selected_tab}.{selected_tab}_app")
module.run()
