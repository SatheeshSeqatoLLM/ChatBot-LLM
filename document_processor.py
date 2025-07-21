
import docx
import pytesseract
from pypdf import PdfReader

def get_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    try:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

def get_docx_text(docx_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        return f"Error reading DOCX file: {e}"

def get_text_from_file(file_path):
    """Extract text from a file based on its extension."""
    if file_path.endswith(".pdf"):
        return get_pdf_text(file_path)
    elif file_path.endswith(".docx"):
        return get_docx_text(file_path)
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as f:
            return f.read()
    else:
        return "Unsupported file type."
