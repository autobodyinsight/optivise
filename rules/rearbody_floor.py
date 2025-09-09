import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["repair", "rpr"]
REAR_BODY_IDENTIFIERS = ["rear body panel"]

SUGGESTIONS = [
    "floor pull w/set up (if needed)",
    "weld tabs for pulls (if needed)",
    "r&i wiring (if needed)",
    "r&i LT trunk trim",
    "r&i L trunk trim",
    "r&i RT trunk trim",
    "r&i R trunk trim",
    "r&i rear body trim",
    "r&i floor cover",
    "r&i spare tire (if needed)"
]

def rearbody_floor_rule(lines, seen):
    print("🚀 rearbody_floor_rule fired")
    triggered = False
    section_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        section_lines.append(line)
        print(f"[REARBODY FLOOR RULE] Scanning line: {norm}")

        if "rear body panel" in norm and any(op in norm for op in REPAIR_OPS):
            triggered = True
            print(f"[REARBODY FLOOR RULE] ✅ Triggered on line: {line}")
            break

    if not triggered:
        return None

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[REARBODY FLOOR RULE] 🎯 Suggestions returned: {missing}")
        return ("REAR BODY + FLOOR REPAIR CHECK", missing)

    return None

def register():
    print("✅ rearbody_floor_rule registered")
    return [rearbody_floor_rule]