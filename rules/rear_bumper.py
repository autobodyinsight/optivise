import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["rpr", "repair", "rep"]
REAR_PARTS = [
    "bumper", "bumper cover", "fascia",
    "bumper cover assembly", "bumper cover assy"
]

WARNING = ["WARNING! VERIFY REPAIR IS NOT WITHIN RADAR LINE OF SITE"]

# Precompile adjacent repair + bumper patterns
REPAIR_BUMPER_PATTERNS = [
    rf"\b{op}\s+{part}\b"
    for op in REPAIR_OPS
    for part in REAR_PARTS
]

def rear_bumper_rule(lines, seen):
    in_rear_section = False

    for line in lines:
        stripped = line.strip()

        # Detect section start: allow numbered or mixed-case headers
        if "REAR" in stripped.upper() and "BUMPER" in stripped.upper():
            in_rear_section = True
            continue

        # Exit section only if a new unrelated all-caps header appears
        if in_rear_section and stripped.isupper() and not ("REAR" in stripped or "BUMPER" in stripped):
            in_rear_section = False
            continue

        if in_rear_section:
            norm = normalize_operation(normalize_orientation(line))

            # Check for adjacent repair + bumper term
            adjacent_match = any(re.search(pattern, norm) for pattern in REPAIR_BUMPER_PATTERNS)

            if adjacent_match:
                print("REAR BUMPER RULE FIRED ON:", line)
                if WARNING[0] not in seen:
                    return ("REAR BUMPER REPAIR DETECTED", WARNING)

    return None

def register():
    return [rear_bumper_rule]