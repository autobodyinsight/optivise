import re
from utils import normalize

REPAIR_OPS = [
    "remove / install", "r&i", "remove / replace", "repl"
]

HEADLIGHT_TERMS = [
    "headlamp assy", "front combination lamp", "frt combination lamp"
]

VERIFY_OPTIONS = [
    "chrome housing",
    "black housing",
    "halogen",
    "xenon / hid",
    "projector lens",
    "with day time running lamps",
    "with led"
]

def headlamp_rule(lines, seen):
    for line in lines:
        norm = normalize(line)

        # Match any repair op and any headlight term in the same line, regardless of order
        op_found = any(re.search(rf"\b{re.escape(op)}\b", norm) for op in REPAIR_OPS)
        part_found = any(re.search(rf"\b{re.escape(term)}\b", norm) for term in HEADLIGHT_TERMS)

        if op_found and part_found:
            print(f"[HEADLAMP RULE] ✅ Triggered on line: {line}")
            if "With adaptive headlights?" not in seen:
                return (
                    "HEADLAMP VARIANT CHECK",
                    ["With adaptive headlights?"] + ["VERIFY OPTIONS:"] + VERIFY_OPTIONS
                )

    return None

def register():
    return [headlamp_rule]