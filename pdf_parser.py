import re
import pdfplumber
from utils import normalize


def parse_pdf(file_path: str) -> dict:
    raw_lines = []

    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_lines.extend(text.split('\n'))

    # Debug: Print raw lines
    print("📄 Raw lines from PDF:")
    for line in raw_lines:
        print(line)

    # Define keywords to look for
    operations = ["repair", "rpr"]
    parts = ["bumper"]

    parsed_parts = []

    # Parse each line
    for line in raw_lines:
        normalized = normalize(line)
        if any(op in normalized for op in operations) and any(part in normalized for part in parts):
            parsed_parts.append(line)

    return {
        "raw_lines": raw_lines,
        "seen": set(normalize(line) for line in raw_lines),
        "parts": parsed_parts
    }