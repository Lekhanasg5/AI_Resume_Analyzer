def generate_roadmap(required_skills, resume_skills):
    """Generate a basic learning roadmap from missing skills."""

    required = {skill.strip().lower() for skill in required_skills}
    existing = {skill.strip().lower() for skill in resume_skills}

    missing_skills = sorted(required - existing)

    roadmap = []

    for week, skill in enumerate(missing_skills, start=1):
        roadmap.append({
            "Week": f"Week {week}",
            "Skill": skill.title(),
            "Recommendation": f"Learn and practice {skill.title()}."
        })

    return roadmap