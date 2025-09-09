import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

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
    mitchell_triggered = False

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))

        # 🔍 Standard CCC-style detection
        op_found = any(re.search(rf"\b{re.escape(op)}\b", norm) for op in REPAIR_OPS)
        part_found = any(re.search(rf"\b{re.escape(term)}\b", norm) for term in HEADLIGHT_TERMS)

        if op_found and part_found:
            print(f"[HEADLAMP RULE] ✅ Standard trigger on line: {lines[i]}")
            if "With adaptive headlights?" not in seen:
                return (
                    "HEADLAMP VARIANT CHECK",
                    ["IF ADAPTIVE HEADLIGHTS, ADD CALIBRATION"] + ["VERIFY OPTIONS:"] + VERIFY_OPTIONS
                )

        # 🔍 Mitchell-style pairing detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))

            # Case 1: lamp / install → front combination + remove
            if "lamp / install" in norm and "front combination" in prev_norm and "remove" in prev_norm:
                mitchell_triggered = True
                print(f"[HEADLAMP RULE] ✅ Mitchell-style trigger: lamp / install + front combination at index {i-1}/{i}")
                break

            # Case 2: assembly / replace → frt combination + remove
            if "assembly / replace" in norm and "frt combination" in prev_norm and "remove" in prev_norm:
                mitchell_triggered = True
                print(f"[HEADLAMP RULE] ✅ Mitchell-style trigger: assembly / replace + frt combination at index {i-1}/{i}")
                break

    if mitchell_triggered:
        if "With adaptive headlights?" not in seen:
            return (
                "HEADLAMP VARIANT CHECK",
                ["IF ADAPTIVE HEADLIGHTS, ADD CALIBRATION"] + ["VERIFY OPTIONS:"] + VERIFY_OPTIONS
            )

    return None

def register():
    return [headlamp_rule]