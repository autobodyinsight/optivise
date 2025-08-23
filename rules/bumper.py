import re
from utils import normalize, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
FRONT_BUMPER_PARTS = [
    "front bumper", "front bumper cover", "front fascia", "front facebar",
    "front bumper assy", "front bumper assembly"
]

MISSED_ITEMS = [
    "bumper repair kit",
    "flex additive",
    "mask for texture (if applicable)",
    "mask for two tone (if applicable)",
    "ADD for front parking sensors (if applicable)",
    "ADD for front auto park (if applicable)",
    "ADD for front headlamp washers (if applicable)"
]

def bumper_rule(lines, seen):
    for line in lines:
        normalized = normalize(line)
        words = normalized.split()

        op_found = any(op in words for op in REPAIR_OPS)
        part_found = any(re.search(rf"\b{re.escape(part.lower())}\b", normalized) for part in FRONT_BUMPER_PARTS)

        if op_found and part_found:
            suggestions = suggest_if_missing(lines, MISSED_ITEMS, seen)
            if suggestions:
                return ("FRONT BUMPER REPAIR", suggestions)

    return None

def register():
    return [bumper_rule]