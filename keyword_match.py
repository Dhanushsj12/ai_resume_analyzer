from rapidfuzz import fuzz

# Master Skill Database
MASTER_SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript",
    "HTML", "CSS", "React", "Angular", "Vue", "Node.js",
    "Express", "Flask", "Django", "FastAPI",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Firebase",
    "Oracle", "Docker", "Kubernetes",
    "AWS", "Azure", "GCP",
    "Git", "GitHub", "Linux",
    "REST API", "Postman",
    "TensorFlow", "PyTorch", "OpenCV",
    "Machine Learning", "Deep Learning",
    "Artificial Intelligence",
    "Generative AI", "Gemini", "ChatGPT",
    "Pandas", "NumPy", "Scikit-learn",
    "Power BI", "Excel"
]


def extract_jd_skills(job_description):

    jd_lower = job_description.lower()

    skills = []

    for skill in MASTER_SKILLS:

        if skill.lower() in jd_lower:
            skills.append(skill)

    return sorted(list(set(skills)))


def keyword_match(parsed_resume, job_description):

    resume_skills = set(
        skill.lower()
        for skill in parsed_resume["skills"]
    )

    jd_skills = extract_jd_skills(job_description)

    matched = []

    missing = []

    for skill in jd_skills:

        found = False

        for resume_skill in resume_skills:

            similarity = fuzz.ratio(
                skill.lower(),
                resume_skill
            )

            if similarity >= 85:
                found = True
                break

        if found:
            matched.append(skill)

        else:
            missing.append(skill)

    total = len(jd_skills)

    if total == 0:

        percentage = 100

    else:

        percentage = round(
            len(matched) / total * 100,
            2
        )

    return {

        "resume_match_score": percentage,

        "matched_skills": matched,

        "missing_skills": missing,

        "total_keywords": total,

        "matched_keywords": len(matched)
    }