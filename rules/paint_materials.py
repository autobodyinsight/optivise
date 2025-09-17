import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

TRIGGER_TERMS = ["body labor", "paint labor"]
SUGGESTIONS = [
    "cover car",
    "mask jambs",
    "gravel guard",
    "tint",
    "spray out",
    "colorsand and buff",
    "denib and polish",
    "mask wshield",
    "mask backglass",
    "blend roof rail"
]

def paint_materials_rule(lines, seen):
    print("🚀 paint_materials_rule fired")
    triggered = False
    section_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        section_lines.append(line)

        if any(term in norm for term in TRIGGER_TERMS):
            triggered = True
            print(f"[PAINT MATERIALS RULE] ✅ Triggered on line: {line}")
            break

    if not triggered:
        return None

    # Conditional logic based on line content
    notes = " ".join(lines).lower()
    if "roof rail blend" in notes or "blend roof rail" in notes:
        SUGGESTIONS.extend(["mask wshield", "mask backglass", "blend roof rail"])
    if "quarter repair" in notes:
        SUGGESTIONS.extend(["mask backglass", "blend roof rail"])

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[PAINT MATERIALS RULE] 🎯 Suggestions returned: {missing}")
        return ("PAINT MATERIALS CHECK", missing)

    return None

def register():
    print("✅ paint_materials_rule registered")
    return [paint_materials_rule]
