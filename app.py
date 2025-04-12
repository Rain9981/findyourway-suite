import streamlit as st
import importlib
import os

# ✅ Page Setup
st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# ✅ Branded Header (Logo + Title + Subtitle + Globe)
st.markdown("""
<div style='text-align:center; padding-bottom:20px;'>

    <!-- Logo -->
    <img src='https://raw.githubusercontent.com/Rain9981/findyourway-suite/main/assets/findyourway_logo.jpg'
         width='200' style='margin-bottom:10px;' alt='Find Your Way Logo'>

    <!-- Title -->
    <h1 style='color:#800020; font-size: 44px; font-weight: bold; margin-bottom: 8px;'>Find Your Way</h1>

    <!-- Subtitle -->
    <p style='font-size:20px; color:#000000; font-weight:300; margin-top:0;'>Network Marketing Consultants</p>

    <!-- Globe Image -->
    <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Blue_Marble_2001.png/300px-Blue_Marble_2001.png'
         width='65' alt='Satellite Globe' style='margin-top:10px;' />

</div>
""", unsafe_allow_html=True)

# 🔐 Login Setup
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
            st.rerun()
        elif password == "premium":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "premium"
            st.rerun()
        elif password == "elite":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "elite"
            st.rerun()
        elif password == "basic":
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = "basic"
            st.rerun()
        else:
            st.error("Invalid login")
    st.stop()

# ✅ Sidebar Role Display
st.sidebar.mark
