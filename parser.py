import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Common technical skills
COMMON_SKILLS = {
    "python","java","c","c++","c#","javascript","typescript",
    "html","css","react","angular","vue","node.js","express",
    "flask","django","fastapi","spring","sql","mysql","postgresql",
    "mongodb","firebase","oracle","docker","kubernetes","aws",
    "azure","gcp","linux","git","github","jenkins","terraform",
    "tensorflow","pytorch","opencv","pandas","numpy","scikit-learn",
    "machine learning","deep learning","artificial intelligence",
    "gen ai","generative ai","gemini","chatgpt","rest api",
    "postman","redis","graphql","power bi","excel"
}

SECTION_HEADERS = [
    "education",
    "experience",
    "projects",
    "skills",
    "certifications",
    "internships",
    "achievements",
    "summary",
    "objective",
    "technical skills",
    "work experience"
]


def extract_name(text):
    """
    Extract person's name using spaCy.
    """

    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    lines = text.split("\n")

    for line in lines[:5]:
        line = line.strip()
        if len(line.split()) <= 4 and len(line) > 2:
            return line

    return "Not Found"


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    pattern = r'(\+?\d[\d\s\-\(\)]{8,15}\d)'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_linkedin(text):

    pattern = r"https?://(?:www\.)?linkedin\.com/in/[^\s]+"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_github(text):

    pattern = r"https?://(?:www\.)?github\.com/[^\s]+"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_skills(text):

    text_lower = text.lower()

    skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in text_lower:

            skills.append(skill.title())

    return sorted(list(set(skills)))


def extract_section(text, header):

    pattern = rf"{header}(.*?)(education|experience|projects|skills|certifications|internships|achievements|summary|objective|technical skills|$)"

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:

        return match.group(1).strip()

    return ""


def parse_resume(resume_text):

    parsed = {

        "name": extract_name(resume_text),

        "email": extract_email(resume_text),

        "phone": extract_phone(resume_text),

        "linkedin": extract_linkedin(resume_text),

        "github": extract_github(resume_text),

        "skills": extract_skills(resume_text),

        "education": extract_section(
            resume_text,
            "education"
        ),

        "experience": extract_section(
            resume_text,
            "experience"
        ),

        "projects": extract_section(
            resume_text,
            "projects"
        ),

        "certifications": extract_section(
            resume_text,
            "certifications"
        )
    }

    return parsed