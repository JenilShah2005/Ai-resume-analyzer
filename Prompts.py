def get_Score_prompt(resume, Job_Description):
    prompt = f"""
    Your are an expert Resume Analyzer. Your Job is to analyze the resume and job description.
    Based on the analysis you did you need to score the Resume of the user and return the score along with What is missing and what is something that is not necessary in the resume based on the job description. The score should be between 0 and 100.
    And also You need to provide that on what should the I focus more on my resume and what should I remove from my resume based on the job description.
    The Scores should be strict not misleading and the main focus should be on skill set and then on project and experience and at last on achivements and education. If the resume is perfect then the score should be 100 and if the resume is very bad then the score should be 0. The score should be based on how much the resume is matching with the job description and how much it is not matching with the job description.
    Resume: {resume}
    
    Job Description: {Job_Description}
    
    Please provide the score along with the missing and unnecessary elements strictly in an jason format like this:
    {{
        "score": 0,
        "missing_elements": [],
        "unnecessary_elements": [],
        "focus_on": [],
    }}
    """
    return prompt