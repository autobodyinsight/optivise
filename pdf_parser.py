import re
import pdfplumber
from utils import normalize

def parse_pdf(file_path: str) -> dict:
    raw_lines = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_lines.extend(text.split('\n'))

    print("📄 Raw lines from PDF:")
    for line in raw_lines:
        print(line)

    # 🔍 Insert this block right here to detect headers
    for line in raw_lines:
        if line.isupper() and len(line.strip().split()) <= 3:
            print("🔹 Detected header:", line)

    operations = ["repair", "rpr"]
    parts = ["bumper"]

    parsed_parts = []

    for line in raw_lines:
        normalized = normalize(line)
        if any(op in normalized for op in operations) and any(part in normalized for part in parts):
            parsed_parts.append(line)

    headers = [line for line in raw_lines if line.isupper() and len(line.strip().split()) <= 3]

    return {
    "raw_lines": raw_lines,
    "seen": set(normalize(line) for line in raw_lines),
    "parts": parsed_parts,
    "headers": headers  # ✅ Add this line
}