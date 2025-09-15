import re
from utils import normalize, normalize_orientation, normalize_operation

# 🔍 Target keywords
TARGET_KEYWORDS = [
    "lt outer panel", "rt outer panel",
    "lt quarter panel", "rt quarter panel",
    "rear body panel", "floor pan"
]

def identify_material_lines(lines):
    matched_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        for keyword in TARGET_KEYWORDS:
            if normalize(keyword) in norm:
                matched_lines.append(line)
                print(f"[IDENTIFY] ✅ Matched keyword '{keyword}' in line: {line}")
                break  # Avoid duplicate matches for same line

    return matched_lines

def register():
    print("✅ identify_material_lines registered")
    return [identify_material_lines]
