import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["repair", "rpr"]
DOOR_IDENTIFIERS = [
    "outer panel",
    "frt door repair panel"
]

REQUIRED_ALIASES = {
    "r&i belt molding": ["belt molding", "belt mldg"],
    "r&i mirror (IF FRONT DOOR)": ["mirror", "side mirror"],
    "r&i handle": ["door handle", "handle"],
    "r&i trim panel": ["trim panel", "door trim", "door trim panel"],
    "r&i molding": ["molding", "door molding"]
}

CONDITIONAL_ALIASES = {
    "r&i run channel (if by design)": ["run channel"],
    "r&i door glass (if by design)": ["door glass", "glass"],
    "r&i carrier (if by design)": ["carrier", "glass carrier"]
}

def door_repair_rule(lines, seen):
    triggered = False
    mitchell_triggered = False
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])

        # 🔍 Standard CCC-style detection
        if any(idf in norm for idf in DOOR_IDENTIFIERS):
            if any(op in norm for op in REPAIR_OPS) or "rpr lt outer panel" in norm:
                triggered = True
                print(f"[DOOR REPAIR] ✅ Standard trigger on line: {lines[i]}")
                break

        # 🔍 Mitchell-style pairing detection (ONLY / replace)
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and "frt door repair panel" in prev_norm:
                if "/ replace" in norm:
                    mitchell_triggered = True
                    print(f"[DOOR REPAIR] ✅ Mitchell-style trigger matched at index {i-1}/{i}")
                    break

    if not triggered and not mitchell_triggered:
        return None

    missing_required = []
    for label, aliases in REQUIRED_ALIASES.items():
        present = any(
            any(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in section_lines
        )
        if not present and label not in seen:
            missing_required.append(label)

    missing_conditional = []
    for label, aliases in CONDITIONAL_ALIASES.items():
        present = any(
            any(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in section_lines
        )
        if not present and label not in seen:
            missing_conditional.append(label)

    suggestions = missing_required + missing_conditional
    if suggestions:
        print(f"[DOOR REPAIR] 🎯 Suggestions returned: {suggestions}")
        return ("DOOR REPAIR ACCESSORY CHECK", suggestions)

    return None

def register():
    print("✅ door_repair_rule registered")
    return [door_repair_rule]