import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_OPS = ["repl"]
REAR_BODY_IDENTIFIERS = ["rear body panel"]

SUGGESTIONS = [
    "adjacent repair LT quarter panel",
    "adjacent repair L quarter panel",
    "adjacent repair LT quarter outer panel",
    "adjacent repair L quarter outer panel",
    "adjacent repair RT quarter panel",
    "adjacent repair R quarter panel",
    "adjacent repair RT quarter outer panel",
    "adjacent repair R quarter outer panel",
    "adjacent floor repair",
    "r&i LT trunk trim",
    "r&i L trunk trim",
    "r&i RT trunk trim",
    "r&i R trunk trim",
    "r&i rear body panel trim",
    "r&i floor cover",
    "r&i LT tail lamp assy",
    "r&i L tail lamp assy",
    "r&i LT rear combination lamp",
    "r&i L rear combination lamp",
    "r&i RT tail lamp assy",
    "r&i R tail lamp assy",
    "r&i RT rear combination lamp",
    "r&i R rear combination lamp",
    "floor pull w/set up",
    "weld tabs for pulls"
]

def rearbody_repl_rule(lines, seen):
    print("🚀 rearbody_repl_rule fired")
    triggered = False
    section_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        section_lines.append(line)
        print(f"[REARBODY REPL RULE] Scanning line: {norm}")

        if "rear body panel" in norm and any(op in norm for op in REPLACE_OPS):
            triggered = True
            print(f"[REARBODY REPL RULE] ✅ Triggered on line: {line}")
            break

    if not triggered:
        return None

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[REARBODY REPL RULE] 🎯 Suggestions returned: {missing}")
        return ("REAR BODY PANEL REPLACEMENT CHECK", missing)

    return None

def register():
    print("✅ rearbody_repl_rule registered")
    return [rearbody_repl_rule]