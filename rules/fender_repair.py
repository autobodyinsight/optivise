import re
from utils import normalize, suggest_if_missing

OPS = ["rpr", "repair", "rep"]
PARTS = ["fender", "fndr"]
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
    norm_lines = [normalize(line) for line in lines]
    suggestions = []

    for norm in norm_lines:
        words = norm.split()

        # Detect repair operation + fender part
        if any(op in words for op in OPS) and any(part in words for part in PARTS):
            # Check if any accessory item is already mentioned in the same line
            if not any(accessory in norm for accessory in ACCESSORY_ITEMS):
                print(f"[FENDER REPAIR] Match found without accessories: {norm}")
                # Suggest missing accessories not already present in the estimate
                suggestions = suggest_if_missing(lines, ACCESSORY_ITEMS, seen)
                break  # Fire once per match

    if suggestions:
        return ("FENDER REPAIR ACCESSORY CHECK", suggestions)

    return None

def register():
    return [fender_repair]