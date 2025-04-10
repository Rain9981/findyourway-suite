import streamlit as st

def run():
    st.title("💼 Subscription Plans Overview")

    st.sidebar.header("💡 Subscription Plans Guide")
    st.sidebar.markdown("""
    - **What this tab does:** Shows the features and pricing for each subscription level.
    - **What to input:** Nothing. This tab is static and shows the plan details.
    - **How to use:** Compare plan levels and use in sales pages or onboarding.
    """)

    st.markdown("## 📦 Plan Levels")

    st.success("""
    **🟢 Basic – $19.99/month**
    - Branding Tools  
    - Forecasting  
    - Strategic Guidance  

    **🔵 Elite – $49.99/month**
    - Everything in Basic  
    - CRM Dashboard  
    - Lead Generation  
    - Marketing Planner  
    - Business Model Canvas  

    **🟣 Premium – $99.99/month**
    - Everything in Elite  
    - Full Suite Access  
    - GPT Autofill + PDF Export  
    - Data Save to Google Sheets  

    **🔐 Admin**
    - All Access  
    - Export CRM / Reports  
    - Edit Plans / View Client Data  
    """)
