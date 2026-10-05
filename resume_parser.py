from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    """Extract text from all pages of a PDF file."""
    reader = PdfReader(file)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    document = Document(file)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_resume_text(file, file_name):
    """Extract resume text based on the uploaded file type."""

    file_name = file_name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")