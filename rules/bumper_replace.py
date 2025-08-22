import re
from utils import normalize, suggest_if_missing

REPLACE_OPS = [
    "repl", "replace", "remove / replace", "remove and replace", "r&r"
]

BUMPER_PARTS = [
    "bumper", "bumper cover", "fascia", "facebar", "bumper assy", "bumper assembly"
]

MISSED_ITEMS = [
    "adhesion promoter",
    "flex additive",
    "mask for texture (if applicable)",
    "mask for two tone (if applicable)",
    "IF APPLICABLE: add for parking sensors",
    "IF APPLICABLE: add for auto park",
    "IF APPLICABLE: add for headlamp washers"
]

def contains_exact_keyword(norm_line, keywords):
    return any(re.search(rf"\b{re.escape(k)}\b", norm_line) for k in keywords)

def bumper_replace_rule(lines, seen):
    for line in lines:
        norm_line = normalize(line)

        op_found = contains_exact_keyword(norm_line, REPLACE_OPS)
        part_found = contains_exact_keyword(norm_line, BUMPER_PARTS)

        if op_found and part_found:
            suggestions = suggest_if_missing(lines, MISSED_ITEMS, seen)
            return ("BUMPER_REPLACE", suggestions or [])

    return None

def register():
    return [bumper_replace_rule]