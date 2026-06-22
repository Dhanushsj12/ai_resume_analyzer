# AI Resume Analyzer & ATS Job Matcher

AI-powered Resume Analyzer built using Flask, Gemini AI, PyPDF2, and Tailwind CSS.

## Features

* ATS Resume Score Analysis
* Resume vs Job Description Matching
* Missing Skills Detection
* Matching Skills Identification
* Resume Improvement Suggestions
* Interview Readiness Assessment
* Learning Roadmap Generation
* PDF Resume Upload
* Gemini AI Powered Analysis

## Tech Stack

* Python
* Flask
* Gemini 2.5 Flash
* PyPDF2
* HTML
* Tailwind CSS
* REST APIs

## Project Architecture

1. User uploads resume PDF
2. Resume text extracted using PyPDF2
3. Job Description collected from user
4. Gemini AI analyzes resume
5. ATS score and recommendations generated
6. Results displayed on dashboard

## Screenshots

### Home Page

![Home Page](screenshots/homepage.png)

### Resume Upload

![Resume Upload](screenshots/upload_resume.png)

### Analysis Result

![Analysis Result](screenshots/analysis_result.png)

## Installation

```bash
git clone https://github.com/Dhanushsj12/ai_resume_analyzer.git
cd ai_resume_analyzer
pip install -r requirements.txt
python app.py
```

## Environment Variables

Create a .env file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

## Future Improvements

* Resume PDF Export
* Multiple Resume Comparison
* Interview Question Generator
* Resume Rewrite Suggestions
* Cover Letter Generator
* AI Career Advisor

## Author

Dhanush S J

GitHub: https://github.com/Dhanushsj12
LinkedIn: https://www.linkedin.com/in/dhanush-s-j-034147271
