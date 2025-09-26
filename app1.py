import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from docx import Document

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📄 AI Resume + Job Description Matcher (ATS Optimizer)")

# Upload Resume
resume_file = st.file_uploader("Upload your Resume (DOCX)", type=["docx"])
# Paste Job Description
job_description = st.text_area("Paste Job Description Here")

if st.button("Analyze"):
    if resume_file is not None and job_description.strip() != "":
        # Read Resume Content
        doc = Document(resume_file)
        resume_text = "\n".join([para.text for para in doc.paragraphs])

        # Prompt for AI
        prompt = f"""
        You are an ATS (Applicant Tracking System) analyzer.
        Compare the following resume with the job description.
        Provide:
        1. Match Score (0-100)
        2. Strengths of the Resume
        3. Weaknesses / Missing keywords
        4. Suggested improvements to increase chances of selection

        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """

        with st.spinner("Analyzing resume with job description..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

        st.subheader("📊 ATS Report")
        st.write(response.choices[0].message.content)
    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
