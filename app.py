import streamlit as st
from google import genai
import json
from parser import extract_text_from_pdf
from Prompts import get_Score_prompt


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload Resume and Job Description PDFs for AI analysis."
)

# -------------------------
# API KEY INPUT
# -------------------------

api_key = st.text_input(
    "Enter Gemini API Key",
    type="password"
)

# -------------------------
# MODEL SELECTION
# -------------------------

model_name = st.selectbox(
    "Choose Gemini Model",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-3.5-flash"
    ]
)

# -------------------------
# FILE UPLOADS
# -------------------------

resume_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

jd_file = st.file_uploader(
    "Upload Job Description PDF",
    type=["pdf"]
)

# -------------------------
# ANALYZE BUTTON
# -------------------------

if st.button("Analyze Resume"):

    if not api_key:
        st.error("Please enter Gemini API Key.")

    elif resume_file is None or jd_file is None:
        st.error("Please upload both PDFs.")

    else:

        try:

            # Initialize Gemini Client
            client = genai.Client(
                api_key=api_key
            )

            # Save uploaded files temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(resume_file.read())

            with open("temp_jd.pdf", "wb") as f:
                f.write(jd_file.read())

            # Extract text
            with st.spinner("Extracting PDF text..."):

                resume_text = extract_text_from_pdf(
                    "temp_resume.pdf"
                )

                job_description = extract_text_from_pdf(
                    "temp_jd.pdf"
                )

            # Build Prompt
            prompt = get_Score_prompt(
                resume_text,
                job_description
            )

            # Gemini API Call
            with st.spinner("Analyzing with Gemini..."):

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

            # Output
            st.success("Analysis Completed!")

            st.subheader("Analysis Result")
            
            cleaned_response = response.text.strip()

            cleaned_response = cleaned_response.replace(
                "```json",
                ""
            )

            cleaned_response = cleaned_response.replace(
                "```",
                ""
            )

            cleaned_response = cleaned_response.strip()

            try:
                result = json.loads(cleaned_response)

            except json.JSONDecodeError:

                st.error("Gemini returned invalid JSON.")

                st.code(cleaned_response)

                st.stop()
            st.subheader("Resume Match Score")
            st.metric( 
                label = "",
                value=f"{result['score']}%"
            )
            st.subheader("Missing Elements")
            if result["missing_elements"]:
                for elem in result["missing_elements"]:
                    st.write(f"- {elem}")

            st.subheader("Unnecessary Elements")
            if result["unnecessary_elements"]:
                for elem in result["unnecessary_elements"]:
                    st.write(f"- {elem}")
                    
            st.subheader("Focus Areas")
            if result["focus_on"]:
                for elem in result["focus_on"]:
                    st.write(f"- {elem}")
                    
        except Exception as e:

            st.error(f"Error: {str(e)}")