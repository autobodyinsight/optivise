import re
from utils import normalize, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
FENDER_PARTS = ["fender", "fender panel", "fndr"]

# Canonical suggestions
ACCESSORY_ITEMS = [
    "r&i fender liner",
    "r&i wheel opening molding",
    "r&i mud guard",
    "r&i LT corner molding",
    "r&i RT corner molding",
    "r&i LT rocker molding",
    "r&i RT rocker molding"
]

# Aliases for matching
ACCESSORY_ALIASES = {
    "r&i fender liner": ["r&i fender liner"],
    "r&i wheel opening molding": ["r&i wheel opng mldg", "r&i wheel opening molding"],
    "r&i mud guard": ["r&i mud guard"],
    "r&i LT corner molding": ["r&i lt corner molding", "lt corner molding"],
    "r&i RT corner molding": ["r&i rt corner molding", "rt corner molding"],
    "r&i LT rocker molding": ["r&i lt rocker molding", "lt rocker molding", "r&i lt rkr molding", "lt rkr molding"],
    "r&i RT rocker molding": ["r&i rt rocker molding", "rt rocker molding", "r&i rt rkr molding", "rt rkr molding"]
}

def fender_repair(lines, seen):
    found_trigger = False

    for line in lines:
        norm = normalize(line)
        words = norm.split()

        op_found = any(op in words for op in REPAIR_OPS)
        part_found = any(part in norm for part in FENDER_PARTS)

        if op_found and part_found:
            found_trigger = True
            print(f"[FENDER REPAIR] ✅ Triggered on line: {line}")
            break

    if not found_trigger:
        return None

    # Filter out accessories already present
    missing = []
    for label, aliases in ACCESSORY_ALIASES.items():
        present = any(
            normalize(alias) in normalize(line)
            for line in lines
            for alias in aliases
        )
        if not present and label not in seen:
            missing.append(label)

    if missing:
        print(f"[FENDER REPAIR] 🎯 Suggestions returned: {missing}")
        return ("FENDER REPAIR ACCESSORY CHECK", missing)

    return None

def register():
    return [fender_repair]