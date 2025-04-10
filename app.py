import streamlit as st
import importlib
import os

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# ✅ Branding with hosted globe and logo
st.markdown("""
<div style='text-align:center;'>
    <h1>🌍 Find Your Way Network Marketing Consultants</h1>
    <img src='https://raw.githubusercontent.com/Rain9981/findyourway-suite/main/assets/globe.gif' width='100' style='margin-top:10px;' alt='Spinning Globe'>
    <br/>
    <img src='https://findyourway-suite-jglcfcdtomhg8wedv3pkqn.streamlit.app/logo.png' width='200' style='margin-top:15px;' alt='Find Your Way Logo'>
</div>
""", unsafe_allow_html=True)

# 🔐 Login logic with tier access
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = "guest"

if not st.session_state["logged_in"]:
    st.title("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == "FindYourWayNMC520":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "admin"
        elif password == "premium":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "premium"
        elif password == "elite":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "elite"
        elif password == "basic":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "basic"
        else:
            st.error("Invalid login")
        st.rerun()
    st.stop()

# ✅ Sidebar for choosing tool
tab_dirs = [d for d in os.listdir() if os.path.isdir(d) and os.path.exists(f"{d}/{d}_app.py")]
selected = st.sidebar.selectbox("📂 Choose a Tool", sorted(tab_dirs))

# ✅ Dynamic tab loading
module = importlib.import_module(f"{selected}.{selected}_app")
if hasattr(module, "run"):
    module.run()
else:
    st.error(f"⚠️ Tab '{selected}' is missing a run() function.")
