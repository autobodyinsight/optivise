import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
BUMPER_PARTS = [
    "bumper", "bumper cover", "fascia", "facebar",
    "bumper assy", "bumper assembly"
]

MISSED_ITEMS = [
    "mask for texture (if applicable)",
    "mask for two tone (if applicable)",
    "feather, prime, and block",
    "ADD for parking sensors (if applicable)",
    "ADD for auto park (if applicable)",
]

def bumper_rule(lines, seen):
    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        words = norm.split()

        op_found = any(op in words for op in REPAIR_OPS)
        part_found = any(re.search(rf"\b{re.escape(part.lower())}\b", norm) for part in BUMPER_PARTS)

        if op_found and part_found:
            suggestions = suggest_if_missing(lines, MISSED_ITEMS, seen)
            if suggestions:
                return ("BUMPER REPAIR", suggestions)

    return None

def register():
    return [bumper_rule]