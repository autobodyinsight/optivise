import re
from utils import normalize, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
FENDER_PARTS = ["fender", "fender panel", "fndr"]

# Canonical suggestions
ACCESSORY_ITEMS = [
    "r&i fender liner",
    "r&i wheel opng mldg",
    "r&i mud guard",
    "r&i corner molding",
    "r&i rocker molding"
]

# Aliases for matching
ACCESSORY_ALIASES = {
    "r&i fender liner": ["fender liner"],
    "r&i wheel opng mldg": ["wheel opng mldg"],
    "r&i mud guard": ["mud guard"],
    "r&i corner molding": ["corner molding"],
    "r&i rocker molding": ["rocker molding"]
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
        found = any(
            all(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in lines
        )
        if not found and label not in seen:
            missing.append(label)

    if missing:
        print(f"[FENDER REPAIR] 🎯 Suggestions returned: {missing}")
        return ("FENDER REPAIR ACCESSORY CHECK", missing)

    return None

def register():
    return [fender_repair]