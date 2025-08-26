import re
from utils import normalize, suggest_if_missing  # Use shared normalization

OPS = ["rpl", "replace", "remove / replace", "rem / repl"]
PARTS = ["bumper", "bumper cover", "fascia", "bumper cover assy", "bumper cover assembly"]
HEADER = "FRONT BUMPER"

SUGGESTIONS = [
    "flex additive",
    "adhesion promoter",
    "static neutralization",
    "mask for texture",
    "mask for two tone",
    "ADD for parking sensors",
    "ADD for auto park",
    "ADD if required - transfer parking sensor brackets",
    "IF LKQ ADD DETRIM TO ALL BUMPER COMPONENTS"
]

# Precompile adjacent operation + part patterns
REPLACE_PATTERNS = [
    rf"\b{op}\b.*\b{part}\b|\b{part}\b.*\b{op}\b"
    for op in OPS
    for part in PARTS
]

def front_bumper_replace_rule(lines, seen):
    in_front_section = False
    found_match = False
    section_lines = []

    for line in lines:
        norm = normalize(line)

        # Detect section entry
        if HEADER in line:
            in_front_section = True
            print(f"[FRONT BUMPER REPLACE RULE] Entered section: {line.strip()}")
            continue

        # Exit section on new all-caps header
        if re.match(r"^[A-Z ]{5,}$", line.strip()) and HEADER not in line:
            in_front_section = False

        if in_front_section:
            section_lines.append(line)
            print(f"[FRONT BUMPER REPLACE RULE] Scanning line: {norm}")

            for pattern in REPLACE_PATTERNS:
                if re.search(pattern, norm):
                    print(f"[FRONT BUMPER REPLACE RULE] ✅ Match found: {line}")
                    found_match = True

    if found_match:
        missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
        if missing:
            return ("FRONT BUMPER REPLACEMENT CHECK", missing)

    return None

def register():
    return [front_bumper_replace_rule]