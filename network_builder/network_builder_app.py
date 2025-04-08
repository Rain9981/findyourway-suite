import streamlit as st
import pandas as pd





def run():
    st.title("🌐 Network Builder")
    st.markdown("### Build your referral map.")

    partner_name = st.text_input("Partner Name")
    area = st.text_input("Area of Support")
