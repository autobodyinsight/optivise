import re
from utils import normalize, suggest_if_missing

OPS = ["rpr", "repair", "rep"]
PARTS = ["fender", "fndr"]
HEADER = "FENDER"

ACCESSORY_ITEMS = [
    "r&i fender liner",
    "r&i wheel opng mldg",
    "r&i mud guard",
    "r&i corner molding",
    "r&i rocker molding",
    "r&i rkr mldg",
    "r&i rocker mldg",
    "r&i rkr molding"
]

def fender_repair(lines: list[str], seen: set[str]) -> tuple[str, list[str]] | None:
    in_fender_section = False
    found_repair = False

    for line in lines:
        norm = normalize(line)

        # Detect entry into FENDER section
        if HEADER in line:
            in_fender_section = True
            print(f"[FENDER ACCESSORY RULE] Entered section: {line.strip()}")
            continue

        # Exit section if new all-caps header appears
        if re.match(r"^[A-Z ]{5,}$", line.strip()) and HEADER not in line:
            in_fender_section = False

        if in_fender_section:
            # Detect repair operation + fender part
            if any(op in norm for op in OPS) and any(part in norm for part in PARTS):
                found_repair = True
                print(f"[FENDER ACCESSORY RULE] Repair match: {line.strip()}")

    if found_repair:
        suggestions = suggest_if_missing(lines, ACCESSORY_ITEMS, seen)
        if suggestions:
            return ("FENDER REPAIR ACCESSORY CHECK", suggestions)

    return None

def register():
    return [fender_repair]