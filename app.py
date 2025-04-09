import streamlit as st
import importlib
import os

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌍 Branding: spinning businessman + logo
st.markdown("""
<div style='text-align:center;'>
    <h1>🌍 Find Your Way Network Marketing Consultants</h1>
    <img src='https://i.gifer.com/VAyR.gif' width='100'>
    <br/>
    <img src='https://findyourwaynmc.wixsite.com/my-site/_files/ugd/2bd6a2_0a1d305fc8e24ab5b9e26ea5e8f15f60~mv2.png' width='140' style='margin-top:5px;'>
</div>
""", unsafe_allow_html=True)

# 🔐 Login with tier access
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = "guest"

if not st.session_state["logged_in"]:
    st.title("🔐 Login to Find Your Way Suite")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == "FindYourWayNMC520":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "admin"
            st.experimental_rerun()
        elif password == "elite":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "elite"
            st.experimental_rerun()
        elif password == "premium":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "premium"
            st.experimental_rerun()
        elif password == "basic":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "basic"
            st.experimental_rerun()
        else:
            st.error("Invalid password")
    st.stop()

# 🔁 Load dropdown for each valid tab
tab_folders = sorted([
    f for f in os.listdir() if os.path.isdir(f)
    and not f.startswith(".")
    and os.path.exists(f"{f}/{f}_app.py")
])

selected = st.sidebar.selectbox("📂 Choose a Tool", tab_folders)
module = importlib.import_module(f"{selected}.{selected}_app")
module.run()
