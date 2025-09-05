import re
from utils import normalize, suggest_if_missing

REPAIR_KEYWORDS = ["rpr", "repair", "rep"]
FENDER_KEYWORDS = ["fender", "fndr"]

ACCESSORY_ALIASES = {
    "fender liner": ["fender liner"],
    "wheel opening molding": ["wheel opng mldg", "wheel opening molding"],
    "mud guard": ["mud guard"],
    "corner molding": ["corner molding"],
    "rocker molding": ["rocker molding", "rkr molding", "rkr mldg", "rocker mldg"]
}

def normalize_line(text):
    return re.sub(r'[^a-z0-9\s]', '', text.lower())

def contains_keywords(line, keywords):
    norm = normalize_line(line)
    return all(kw in norm for kw in keywords)

def matches_trigger(line):
    return (
        contains_keywords(line, REPAIR_KEYWORDS[:1]) and  # "rpr"
        any(kw in normalize_line(line) for kw in FENDER_KEYWORDS)
    )

def accessory_present(line, aliases):
    norm = normalize_line(line)
    return any(alias in norm for alias in aliases)

def fender_repair(lines: list[str], seen: set[str]) -> tuple[str, list[str]] | None:
    triggered = any(matches_trigger(line) for line in lines)
    if not triggered:
        return None

    suggestions = []
    for label, aliases in ACCESSORY_ALIASES.items():
        found = any(accessory_present(line, aliases) for line in lines)
        if not found and f"r&i {label}" not in seen:
            suggestions.append(f"r&i {label}")

    if suggestions:
        print("[FENDER REPAIR] ✅ Triggered. Missing accessories:", suggestions)
        return ("FENDER REPAIR ACCESSORY CHECK", suggestions)

    return None

def register():
    return [fender_repair]