import re
from utils.matching import normalize_text

REPLACE_OPS = ["replace", "install", "reinstall"]
BUMPER_PARTS = ["bumper cover", "bumper", "bumper assembly"]
EXCLUDED_SUFFIXES = ["rivet", "bracket", "retainer", "clip", "absorber"]

def contains_exact_phrase(norm_line, phrases):
    return any(re.search(rf"\b{re.escape(phrase)}\b", norm_line) for phrase in phrases)

def is_false_positive(norm_line):
    return any(suffix in norm_line for suffix in EXCLUDED_SUFFIXES)

def apply_rule(lines):
    suggestions = []
    for line in lines:
        norm_line = normalize_text(line)

        op_found = contains_exact_phrase(norm_line, REPLACE_OPS)
        part_found = contains_exact_phrase(norm_line, BUMPER_PARTS)

        if op_found and part_found and not is_false_positive(norm_line):
            suggestions.extend([
                "adhesion promoter",
                "IF APPLICABLE: add for parking sensors",
                "IF APPLICABLE: add for auto park",
                "IF APPLICABLE: add for headlamp washers"
            ])
            break  # Only trigger once per doc

    if suggestions:
        return {"rule": "BUMPER_REPLACE", "suggestions": suggestions}
    return None