def match_skills(resume_text, skills):

    found = []
    missing = []

    for skill in skills:
        if skill in resume_text:
            found.append(skill)
        else:
            missing.append(skill)

    score = (len(found) / len(skills)) * 100

    return found, missing, score