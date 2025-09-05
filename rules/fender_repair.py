import re
from utils import normalize, suggest_if_missing

TRIGGER_PATTERNS = [
    r"rpr\s+lt\s+fender",
    r"rpr\s+rt\s+fender",
    r"r\s+fender\s+panel\s+repair",
    r"l\s+fender\s+panel\s+repair"
]

ACCESSORY_ALIASES = {
    "wheel opening molding": ["wheel opng mldg", "wheel opening molding"],
    "rocker molding": ["rocker molding", "rkr molding", "rkr mldg", "rocker mldg"],
    "corner molding": ["corner molding"],
    "fender liner": ["fender liner"],
    "mud guard": ["mud guard"]
}

def normalize_line(text):
    return re.sub(r'[^a-z0-9\s]', '', text.lower())

def matches_trigger(line):
    norm = normalize_line(line)
    return any(re.search(pattern, norm) for pattern in TRIGGER_PATTERNS)

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