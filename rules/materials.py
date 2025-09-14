import re
from utils import normalize

# 🔧 Refinishing materials to suggest
REFINISH_ITEMS = [
    "weldthrough primer", "weld through primer",
    "cavity wax", "corrosion protection",
    "bonding foam", "anti flutter foam",
    "sound deadening pad", "panel bond"
]

# 🔍 Trigger phrases
REPLACE_TRIGGERS = ["repl", "/replace"]
REMOVE_TRIGGERS = ["remove"]
PART_TRIGGERS = [
    "outer panel", "frt door repair panel",
    "quarter outer panel", "rear body panel",
    "floor pan", "rear body floor pan"
]

def materials_rule(lines, seen):
    normalized_lines = [normalize(line) for line in lines]
    triggered_phrases = []

    for idx, norm in enumerate(normalized_lines):
        current_line = norm
        prev_line = normalized_lines[idx - 1] if idx > 0 else ""

        # 🔍 Check if current line is a replacement
        if any(rep in current_line for rep in REPLACE_TRIGGERS):
            # 🔍 Check if previous line is a removal
            if any(rem in prev_line for rem in REMOVE_TRIGGERS):
                # 🔍 Check if either line mentions a target part
                if any(part in current_line for part in PART_TRIGGERS) or any(part in prev_line for part in PART_TRIGGERS):
                    phrase = f"{lines[idx - 1]} → {lines[idx]}" if idx > 0 else lines[idx]
                    triggered_phrases.append(phrase)

    # 🧹 Deduplicate and filter suggestions
    found = set()
    for line in lines:
        norm = normalize(line)
        for item in REFINISH_ITEMS:
            if item in norm:
                found.add(item)

    missing = [item for item in REFINISH_ITEMS if item not in found and item not in seen]

    if missing and triggered_phrases:
        for phrase in triggered_phrases:
            print(f"[MATERIALS] 🔥 Triggered by: {phrase}")
        print(f"[MATERIALS] 🎯 Missing refinishing items: {missing}")
        return ("MATERIALS & REFINISH CHECK", missing)

    return None

def register():
    return [materials_rule]
