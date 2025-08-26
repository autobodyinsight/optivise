import re
from utils import normalize

REPAIR_OPS = ["rpr", "repair", "rep"]
REAR_PARTS = [
    "bumper", "bumper cover", "fascia",
    "bumper cover assembly", "bumper cover assy"
]

WARNING = ["WARNING! VERIFY REPAIR IS NOT WITHIN RADAR LINE OF SITE"]

def rear_bumper_rule(lines, seen):
    in_rear_section = False

    for line in lines:
        # Detect exact all-caps header
        if line.strip() == "REAR BUMPER":
            in_rear_section = True
            continue

        # Exit section if another all-caps header appears
        if in_rear_section and line.isupper() and line.strip() != "REAR BUMPER":
            break

        if in_rear_section:
            normalized = normalize(line)
            words = normalized.split()

            op_found = any(op in words for op in REPAIR_OPS)
            part_found = any(re.search(rf"\b{re.escape(part.lower())}\b", normalized) for part in REAR_PARTS)

            if op_found and part_found:
                if WARNING[0] not in seen:
                    return ("REAR BUMPER RADAR CHECK", WARNING)

    return None

def register():
    return [rear_bumper_rule]