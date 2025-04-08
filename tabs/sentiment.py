import streamlit as st
import openai
import pandas as pd
import io

openai.api_key = st.secrets["openai"]["api_key"]

def get_sentiment(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Classify sentiment as Positive, Neutral, or Negative."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def run():
    st.title("🤖 AI-Powered Sentiment Analyzer")
    st.markdown("Analyze customer sentiment from text input or uploaded file using OpenAI.")

    # --- Text Input ---
    topic = st.text_input("Enter a single topic or sentence:")
    if st.button("Analyze Input"):
        if topic:
            result = get_sentiment(topic)
            st.success(f"Sentiment: **{result}**")
        else:
            st.warning("Please enter some text to analyze.")

    # --- File Upload ---
    st.markdown("---")
    st.subheader("📁 Upload File (.txt or .csv with 'Text' column)")
    uploaded_file = st.file_uploader("Upload your file here")

    if uploaded_file:
        if uploaded_file.name.endswith(".txt"):
            lines = uploaded_file.read().decode("utf-8").splitlines()
            df = pd.DataFrame(lines, columns=["Text"])
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            if "Text" not in df.columns:
                st.error("CSV must have a 'Text' column.")
                return
        else:
            st.error("Only .txt or .csv files are supported.")
            return

        if st.button("🔍 Analyze Uploaded Content"):
            with st.spinner("Analyzing..."):
                df["Sentiment"] = df["Text"].apply(get_sentiment)
            st.success("Analysis complete!")
            st.dataframe(df)

            # --- PDF Export (Optional) ---
            if st.button("📄 Export as PDF"):
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas

                buffer = io.BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                text_object = c.beginText(40, 750)
                text_object.setFont("Helvetica", 10)

                for i, row in df.iterrows():
                    text_object.textLine(f"{i+1}. {row['Text']} → {row['Sentiment']}")

                c.drawText(text_object)
                c.showPage()
                c.save()
                buffer.seek(0)

                st.download_button("Download PDF", buffer, file_name="sentiment_report.pdf")

            # --- Optional: Save to Google Sheets ---
            if "google_sheets" in st.secrets:
                from backend.google_sheets import save_sentiment_data
                save_sentiment_data(df)
                st.info("✅ Saved to Google Sheet!")
