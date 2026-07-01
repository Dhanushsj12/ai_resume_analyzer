import re

# ----------------------------
# Contact Information Score
# ----------------------------

def contact_score(parsed):

    score = 0

    if parsed["name"] != "Not Found":
        score += 5

    if parsed["email"] != "Not Found":
        score += 5

    if parsed["phone"] != "Not Found":
        score += 5

    if parsed["linkedin"] != "Not Found":
        score += 5

    if parsed["github"] != "Not Found":
        score += 5

    return score


# ----------------------------
# Education Score
# ----------------------------

def education_score(parsed):

    if parsed["education"]:
        return 10

    return 0


# ----------------------------
# Experience Score
# ----------------------------

def experience_score(parsed):

    if parsed["experience"]:

        words = len(parsed["experience"].split())

        if words > 150:
            return 15

        elif words > 50:
            return 10

        return 5

    return 0


# ----------------------------
# Projects Score
# ----------------------------

def project_score(parsed):

    if parsed["projects"]:

        words = len(parsed["projects"].split())

        if words > 120:
            return 10

        elif words > 40:
            return 8

        return 5

    return 0


# ----------------------------
# Certifications
# ----------------------------

def certification_score(parsed):

    if parsed["certifications"]:
        return 10

    return 0


# ----------------------------
# Skills Score
# ----------------------------

def skill_score(parsed):

    count = len(parsed["skills"])

    if count >= 15:
        return 15

    elif count >= 10:
        return 12

    elif count >= 5:
        return 8

    elif count > 0:
        return 5

    return 0


# ----------------------------
# Resume Length Score
# ----------------------------

def length_score(text):

    words = len(text.split())

    if 300 <= words <= 800:
        return 10

    elif 200 <= words < 300:
        return 8

    elif words > 800:
        return 6

    return 4


# ----------------------------
# Formatting Score
# ----------------------------

def formatting_score(text):

    score = 10

    if "table" in text.lower():
        score -= 2

    if len(text.splitlines()) < 15:
        score -= 3

    return max(score, 0)


# ----------------------------
# Grammar Score
# (placeholder)
# ----------------------------

def grammar_score():

    return 10


# ----------------------------
# Final ATS Score
# ----------------------------

def calculate_ats(parsed, resume_text):

    scores = {

        "contact_score":
            contact_score(parsed),

        "education_score":
            education_score(parsed),

        "experience_score":
            experience_score(parsed),

        "project_score":
            project_score(parsed),

        "certification_score":
            certification_score(parsed),

        "skill_score":
            skill_score(parsed),

        "length_score":
            length_score(resume_text),

        "formatting_score":
            formatting_score(resume_text),

        "grammar_score":
            grammar_score()
    }

    total = sum(scores.values())

    scores["ats_score"] = min(total, 100)

    return scores