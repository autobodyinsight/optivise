import re
from utils import normalize, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
FENDER_PARTS = ["fender", "fender panel", "fndr"]
ACCESSORY_ITEMS = [
    "r&i fender liner",
    "r&i wheel opng mldg",
    "r&i mud guard",
    "r&i LT corner molding",
    "r&i RT corner molding",
    "r&i LT rocker molding",
    "r&i RT rocker molding"
]

# Normalize aliases for matching
ACCESSORY_ALIASES = {
    "r&i wheel opening molding": ["r&i wheel opng mldg", "r&i wheel opening molding"],
    "r&i rocker molding": ["r&i rocker molding", "r&i rkr molding", "r&i rkr mldg", "r&i rocker mldg"],
    "r&i corner molding": ["r&i corner molding"],
    "r&i fender liner": ["r&i fender liner"],
    "r&i mud guard": ["r&i mud guard"]
}

def fender_repair(lines, seen):
    found_trigger = False

    for line in lines:
        norm = normalize(line)
        words = norm.split()

        op_found = any(op in words for op in REPAIR_OPS)
        part_found = any(part in words for part in FENDER_PARTS)

        if op_found and part_found:
            found_trigger = True
            print(f"[FENDER REPAIR] ✅ Triggered on line: {line}")
            break

    if not found_trigger:
        return None

    # Check if any accessory items are already present
    missing = []
    for label, aliases in ACCESSORY_ALIASES.items():
        already_present = any(normalize(line).find(normalize(alias)) != -1 for line in lines for alias in aliases)
        if not already_present and label not in seen:
            missing.append(label)

    if missing:
        print(f"[FENDER REPAIR] 🎯 Suggestions returned: {missing}")
        return ("FENDER REPAIR ACCESSORY CHECK", missing)

    return None

def register():
    return [fender_repair]