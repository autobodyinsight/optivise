import re
from utils import normalize, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
REAR_BUMPER_PARTS = [
    "rear bumper", "rear bumper cover", "rear fascia", "rear facebar",
    "rear bumper assy", "rear bumper assembly"
]

MISSED_ITEMS = [
    "rear bumper repair kit",
    "flex additive",
    "mask for texture (if applicable)",
    "mask for two tone (if applicable)",
    "ADD for rear parking sensors (if applicable)",
    "ADD for rear auto park (if applicable)",
    "ADD for rear headlamp washers (if applicable)"
]

def rear_bumper_rule(lines, seen):
    for line in lines:
        normalized = normalize(line)
        words = normalized.split()

        op_found = any(op in words for op in REPAIR_OPS)
        part_found = any(re.search(rf"\b{re.escape(part.lower())}\b", normalized) for part in REAR_BUMPER_PARTS)

        if op_found and part_found:
            suggestions = suggest_if_missing(lines, MISSED_ITEMS, seen)
            if suggestions:
                return ("REAR BUMPER REPAIR", suggestions)

    return None

def register():
    return [rear_bumper_rule]