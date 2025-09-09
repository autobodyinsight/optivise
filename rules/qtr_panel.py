import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["repair", "rpr"]
QTR_IDENTIFIERS = ["quarter panel", "quarter outer panel"]

SUGGESTIONS = [
    "adjacent repair rocker panel",
    "adjacent repair rear body",
    "adjacent repair floor",
    "blend roof rail",
    "blend rocker panel",
    "blnd roof rail",
    "blnd rocker panel",
    "r&i liner",
    "r&i qtr glass",
    "r&i roof molding",
    "r&i fuel door (if needed)"
]

def qtr_panel_rule(lines, seen):
    print("🚀 qtr_panel_rule fired")
    triggered = False
    mitchell_triggered = False
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[QTR PANEL RULE] Scanning line: {norm}")

        # 🔍 Standard CCC-style detection
        if any(qtr in norm for qtr in QTR_IDENTIFIERS) and any(op in norm for op in REPAIR_OPS):
            triggered = True
            print(f"[QTR PANEL RULE] ✅ Standard trigger on line: {lines[i]}")
            break

        # 🔍 Mitchell-style pairing detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and "quarter outer panel" in prev_norm and "/ replace" in norm:
                mitchell_triggered = True
                print(f"[QTR PANEL RULE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")
                break

    if not triggered and not mitchell_triggered:
        return None

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[QTR PANEL RULE] 🎯 Suggestions returned: {missing}")
        return ("QUARTER PANEL REPAIR CHECK", missing)

    return None

def register():
    print("✅ qtr_panel_rule registered")
    return [qtr_panel_rule]