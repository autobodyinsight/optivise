import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_OPS = ["repl"]
FLOOR_IDENTIFIERS = ["floor pan", "rear body floor pan"]

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

def floor_repl_rule(lines, seen):
    print("🚀 floor_repl_rule fired")
    triggered = False
    mitchell_triggered = False
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[FLOOR REPL RULE] Scanning line: {norm}")

        # 🔍 Standard CCC-style detection
        if any(floor in norm for floor in FLOOR_IDENTIFIERS) and any(op in norm for op in REPLACE_OPS):
            triggered = True
            print(f"[FLOOR REPL RULE] ✅ Standard trigger on line: {lines[i]}")
            break

        # 🔍 Mitchell-style pairing detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and any(floor in prev_norm for floor in FLOOR_IDENTIFIERS) and "/ replace" in norm:
                mitchell_triggered = True
                print(f"[FLOOR REPL RULE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")
                break

    if not triggered and not mitchell_triggered:
        return None

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[FLOOR REPL RULE] 🎯 Suggestions returned: {missing}")
        return ("FLOOR PAN REPLACEMENT CHECK", missing)

    return None

def register():
    print("✅ floor_repl_rule registered")
    return [floor_repl_rule]