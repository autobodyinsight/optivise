import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
REPLACE_OPS = ["replace", "repl", "remove / replace"]
FENDER_PARTS = ["fender", "fender panel", "fndr"]

# Canonical suggestions
ACCESSORY_ITEMS = [
    "r&i fender liner",
    "r&i wheel opening molding",
    "r&i mud guard",
    "r&i corner molding",
    "r&i rocker molding"
]

# Aliases for matching
ACCESSORY_ALIASES = {
    "r&i fender liner": ["fender liner"],
    "r&i wheel opening molding (if equipped)": ["wheel opng mldg", "flare", "wheel opening molding"],
    "r&i mud guard (if equipped)": ["mud guard"],
    "r&i corner molding (if equipped)": ["corner molding", "corner mldg"],
    "r&i rocker molding (if equipped)": ["rocker molding", "rkr molding", "rocker mldg", "rkr mldg"]
}

def fender_repair(lines, seen):
    triggered = False
    operation_type = None

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        words = norm.split()

        if any(op in words for op in REPAIR_OPS) and any(part in norm for part in FENDER_PARTS):
            triggered = True
            operation_type = "REPAIR"
            print(f"[FENDER REPAIR] ✅ Triggered on line: {line}")
            break

        if any(op in norm for op in REPLACE_OPS) and any(part in norm for part in FENDER_PARTS):
            triggered = True
            operation_type = "REPLACEMENT"
            print(f"[FENDER REPLACEMENT] ✅ Triggered on line: {line}")
            break

    if not triggered:
        return None

    # Filter out accessories already present
    missing = []
    for label, aliases in ACCESSORY_ALIASES.items():
        present = any(
            any(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in lines
        )
        if not present and label not in seen:
            missing.append(label)

    if missing:
        title = f"FENDER {operation_type} ACCESSORY CHECK"
        print(f"[FENDER {operation_type}] 🎯 Suggestions returned: {missing}")
        return (title, missing)

    return None

def register():
    return [fender_repair]