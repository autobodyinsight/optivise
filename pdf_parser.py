import re
import pdfplumber
from utils import normalize

def merge_stacked_operations(lines: list[str]) -> list[str]:
    merged = []
    skip_next = False

    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue

        current = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        current_clean = current.lower()
        next_clean = next_line.lower()

        # Detect stacked operation: current ends in 'remove' or 'install', next contains '/' and a verb
        if any(current_clean.endswith(op) for op in ["remove", "install"]) and re.search(r"/\s*(replace|install|remove)", next_clean):
            combined = f"{current} {next_line.strip()}"
            print(f"[MERGE] Combined stacked line: {combined}")
            merged.append(combined)
            skip_next = True
        else:
            merged.append(current)

    return merged

def parse_pdf(file_path: str) -> dict:
    raw_lines = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_lines.extend(text.split('\n'))
    raw_lines = merge_stacked_operations(raw_lines)

    print("📄 Raw lines from PDF:")
    for line in raw_lines:
        print(f"[LINE] {line}")


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
        norm = normalize(line)
        if any(op in norm for op in operations) and any(part in norm for part in parts):
            parsed_parts.append(line)

    headers = [line for line in raw_lines if line.isupper() and len(line.strip().split()) <= 3]

    return {
    "raw_lines": raw_lines,
    "seen": set(normalize(line) for line in raw_lines),
    "parts": parsed_parts,
    "headers": headers  # ✅ Add this line
}