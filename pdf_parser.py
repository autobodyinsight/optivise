import re
import pdfplumber
from utils import normalize

def parse_pdf(file_path: str) -> dict:
    raw_lines = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            for word in page.extract_words(extra_attrs=["fontname"]):
                text = word["text"].strip()
                font = word.get("fontname", "").lower()
                is_bold = "bold" in font or "bd" in font
                raw_lines.append({"text": text, "is_bold": is_bold})

    print("📄 Raw lines from PDF:")
    for item in raw_lines:
        print(f"{'[BOLD]' if item['is_bold'] else '[PLAIN]'} {item['text']}")

    operations = ["repair", "rpr"]
    parts = ["bumper"]

    parsed_parts = [
        item["text"] for item in raw_lines
        if any(op in normalize(item["text"]) for op in operations)
        and any(part in normalize(item["text"]) for part in parts)
    ]

    return {
        "raw_lines": raw_lines,
        "seen": set(normalize(item["text"]) for item in raw_lines),
        "parts": parsed_parts
    }