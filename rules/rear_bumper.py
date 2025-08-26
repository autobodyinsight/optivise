import re
from utils import normalize

REAR_BUMPER_KEYWORDS = ["rear bumper"]
REPAIR_OPS = ["rpr", "repair", "rep"]
REAR_PARTS = [
    "bumper", "bumper cover", "fascia",
    "bumper cover assembly", "bumper cover assy"
]

WARNING = ["WARNING! VERIFY REPAIR IS NOT WITHIN RADAR LINE OF SITE"]

def rear_bumper_rule(lines, seen):
    for line in lines:
        normalized = normalize(line)
        words = normalized.split()

        context_found = any(k in normalized for k in REAR_BUMPER_KEYWORDS)
        op_found = any(op in words for op in REPAIR_OPS)
        part_found = any(re.search(rf"\b{re.escape(part.lower())}\b", normalized) for part in REAR_PARTS)

        if context_found and op_found and part_found:
            if WARNING[0] not in seen:
                return ("REAR BUMPER RADAR CHECK", WARNING)

    return None

def register():
    return [rear_bumper_rule]