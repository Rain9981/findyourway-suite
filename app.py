import streamlit as st
import importlib
import os

st.set_page_config(page_title="Find Your Way Consulting Suite", layout="wide")

# 🌍 Branding
st.markdown(
    "<div style='text-align:center;'>"
    "<h1>🌍 Find Your Way Network Marketing Consultants</h1>"
    "<img src='https://i.gifer.com/VAyR.gif' width='100' style='margin-top:10px;'>"
    "</div>",
    unsafe_allow_html=True
)

# 🔄 Load sidebar dropdown
tabs = sorted([f for f in os.listdir() if os.path.isdir(f) and not f.startswith(".") and os.path.exists(f"{f}/{f}_app.py")])
selected = st.sidebar.selectbox("📂 Choose a Tool", tabs)

module = importlib.import_module(f"{selected}.{selected}_app")
module.run()
