import pandas as pd


def load_skill_dictionary(path="data/skill_dictionary.csv"):
    """Load the skill dictionary from CSV."""
    return pd.read_csv(path)


def extract_skills(text, skill_dictionary):
    """Find skills present in the cleaned resume text."""

    text = text.lower()

    found_skills = []

    for _, row in skill_dictionary.iterrows():
        skill = str(row["Skill"])
        skill_lower = skill.lower()

        if skill_lower in text:
            found_skills.append(
                {
                    "Skill": skill,
                    "Category": row["Category"]
                }
            )

    return pd.DataFrame(found_skills)


def get_skill_names(skill_dataframe):
    """Return only the skill names as a list."""

    if skill_dataframe.empty:
        return []

    return skill_dataframe["Skill"].tolist()