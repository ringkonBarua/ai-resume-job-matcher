import streamlit as st
import openai
import os
from dotenv import load_dotenv
from docx import Document

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (DOCX only)", type=["docx"])

if uploaded_file is not None:
    doc = Document(uploaded_file)
    resume_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

    st.subheader("🔍 Resume Content:")
    st.write(resume_text[:1000] + "...")  # প্রথম 1000 ক্যারেক্টার দেখাবে

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert career consultant."},
                    {"role": "user", "content": f"Analyze this resume:\n\n{resume_text}\n\nProvide:\n1. Strengths\n2. Weaknesses\n3. Suggestions for improvement"}
                ]
            )
            st.subheader("✅ AI Analysis:")
            st.write(response.choices[0].message.content)
