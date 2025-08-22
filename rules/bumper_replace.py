import re
from utils import normalize, suggest_if_missing

REPLACE_OPS = ["repl", "replace", "remove / replace", "remove and replace", "r&r"]
BUMPER_PARTS = ["bumper", "bumper cover", "fascia", "facebar", "bumper assy", "bumper assembly"]

MISSED_ITEMS = [
    "adhesion promoter",
    "flex additive",
    "mask for texture (if applicable)",
    "mask for two tone (if applicable)",
    "ADD for parking sensors (if applicable)",
    "ADD for auto park (if applicable)",
    "ADD for headlamp washers (if applicable)"
]

def bumper_replace_rule(lines, seen):
    for line in lines:
        norm_line = normalize(line)
        if any(op in norm_line for op in REPLACE_OPS) and any(part in norm_line for part in BUMPER_PARTS):
            suggestions = suggest_if_missing(lines, MISSED_ITEMS, seen)
            return ("BUMPER_REPLACE", suggestions or [])
    return None

def register():
    return [bumper_replace_rule]