import pandas as pd
import re


def load_job_roles(path="data/job_roles.csv"):
    """Load job roles and their required skills from CSV."""
    return pd.read_csv(path)


def calculate_match_scores(resume_text, job_roles):
    """Calculate match scores using keyword-based skill matching."""

    resume_text = resume_text.lower()

    results = job_roles.copy()
    scores = []

    for _, row in job_roles.iterrows():

        required_skills = str(row["Required_Skills"]).split(",")

        required_skills = [
            skill.strip().lower()
            for skill in required_skills
            if skill.strip()
        ]

        matched_skills = 0

        for skill in required_skills:
            # Match the skill as a phrase/word
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, resume_text):
                matched_skills += 1

        if required_skills:
            score = (matched_skills / len(required_skills)) * 100
        else:
            score = 0

        scores.append(round(score, 2))

    results["Match_Score"] = scores

    return results.sort_values(
        by="Match_Score",
        ascending=False
    ).reset_index(drop=True)