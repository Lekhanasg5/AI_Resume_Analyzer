import re


def clean_text(text):
    """Clean and normalize extracted resume text."""

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Preserve important technical terms
    text = text.replace("c++", "cpp")
    text = text.replace("c#", "csharp")
    text = text.replace(".net", "dotnet")

    # Remove unnecessary characters
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)

    # Remove repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()