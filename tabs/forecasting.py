import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("📈 Revenue Forecasting Tool")
    business_name = st.text_input("Business Name")
    starting_revenue = st.number_input("Starting Monthly Revenue ($)", min_value=0.0, value=1000.0, step=100.0)
    growth_rate = st.slider("Estimated Monthly Growth Rate (%)", 0, 100, 10)

    months = list(range(1, 13))
    revenue = [starting_revenue]
    for _ in months[1:]:
        revenue.append(revenue[-1] * (1 + growth_rate / 100))

    df = pd.DataFrame({
        "Month": [f"Month {m}" for m in months],
        "Projected Revenue": [round(r, 2) for r in revenue]
    })

    st.subheader("📊 Forecast Chart")
    fig, ax = plt.subplots()
    ax.plot(df["Month"], df["Projected Revenue"], marker='o')
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.set_title(f"{business_name or 'Business'} Revenue Forecast")
    st.pyplot(fig)

    st.subheader("📋 Forecast Table")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="forecast.csv", mime="text/csv")
