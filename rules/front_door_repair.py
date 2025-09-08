import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["repair", "rpr"]
FRONT_DOOR_IDENTIFIERS = [
    "frt door repair panel",
    "front door lt door shell",
    "front door rt door shell"
]

REQUIRED_ALIASES = {
    "r&i belt molding": ["belt molding", "belt mldg"],
    "r&i mirror": ["mirror", "side mirror"],
    "r&i handle": ["door handle", "handle"],
    "r&i trim panel": ["trim panel", "door trim", "door trim panel"],
    "r&i molding": ["molding", "door molding"]
}

CONDITIONAL_ALIASES = {
    "r&i run channel (if by design)": ["run channel"],
    "r&i door glass (if by design)": ["door glass", "glass"],
    "r&i carrier (if by design)": ["carrier", "glass carrier"]
}

def front_door_repair_rule(lines, seen):
    triggered = False
    section_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        section_lines.append(line)

        if any(op in norm.split() for op in REPAIR_OPS) and any(idf in norm for idf in FRONT_DOOR_IDENTIFIERS):
            triggered = True
            print(f"[FRONT DOOR REPAIR] ✅ Triggered on line: {line}")
            break

    if not triggered:
        return None

    missing_required = []
    for label, aliases in REQUIRED_ALIASES.items():
        present = any(
            any(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in lines
        )
        if not present and label not in seen:
            missing_required.append(label)

    missing_conditional = []
    for label, aliases in CONDITIONAL_ALIASES.items():
        present = any(
            any(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in lines
        )
        if not present and label not in seen:
            missing_conditional.append(label)

    suggestions = missing_required + missing_conditional
    if suggestions:
        print(f"[FRONT DOOR REPAIR] 🎯 Suggestions returned: {suggestions}")
        return ("FRONT DOOR REPAIR ACCESSORY CHECK", suggestions)

    return None

def register():
    print("✅ front_door_repair_rule registered")
    return [front_door_repair_rule]