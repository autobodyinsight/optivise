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
    section_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        section_lines.append(line)

        # Match estimate-style phrasing
        if any(idf in norm for idf in DOOR_IDENTIFIERS):
            if "rpr" in norm or "repair" in norm or "rpr lt outer panel" in norm:
                triggered = True
                print(f"[DOOR REPAIR] ✅ Triggered on line: {line}")
                break

    if not triggered:
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