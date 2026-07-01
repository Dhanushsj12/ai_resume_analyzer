import google.generativeai as genai


def generate_ai_review(
    model,
    parsed_resume,
    ats_result,
    keyword_result,
    resume_text,
    job_description
):

    prompt = f"""
You are an Expert ATS Resume Reviewer, Senior HR Manager,
Technical Recruiter, Career Coach and Interview Expert.

You are NOT responsible for calculating ATS scores.
The ATS Engine has already calculated them.

========================
ATS ENGINE RESULTS
========================

ATS Score:
{ats_result["ats_score"]}/100

Resume Match:
{keyword_result["resume_match_score"]}%

Matched Skills:
{', '.join(keyword_result["matched_skills"]) if keyword_result["matched_skills"] else "None"}

Missing Skills:
{', '.join(keyword_result["missing_skills"]) if keyword_result["missing_skills"] else "None"}

========================
PARSED RESUME
========================

Name:
{parsed_resume["name"]}

Email:
{parsed_resume["email"]}

Phone:
{parsed_resume["phone"]}

Skills:
{", ".join(parsed_resume["skills"])}

Education:
{parsed_resume["education"]}

Experience:
{parsed_resume["experience"]}

Projects:
{parsed_resume["projects"]}

Certifications:
{parsed_resume["certifications"]}

========================
RESUME
========================

{resume_text}

========================
JOB DESCRIPTION
========================

{job_description}

========================

Return the response in this exact structure.

## Executive Summary

Write a short professional summary.

## Strengths

- Bullet points

## Weaknesses

- Bullet points

## Resume Improvements

- Bullet points

## Project Review

Evaluate the projects.

Mention

Innovation

Technical Difficulty

Industry Relevance

Portfolio Quality

## Missing Skills

Explain why each missing skill matters.

## Interview Readiness

Rate from 0–100.

Explain why.

## Interview Questions

Generate 10 technical interview questions.

## Learning Roadmap

Give a 30-day learning roadmap.

Week 1

Week 2

Week 3

Week 4

## Final Recruiter Opinion

Would you shortlist this candidate?

Explain why.

Do NOT generate ATS Score.

Do NOT generate Resume Match Score.

Use the ATS Engine values already provided.
"""

    response = model.generate_content(prompt)

    return response.text