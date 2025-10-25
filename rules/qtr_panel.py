import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPAIR_OPS = ["repair", "rpr"]
REPLACE_OPS = ["repl"]
QTR_IDENTIFIERS = [
    "quarter panel",
    "quarter outer panel",
    "quarter pnl",
    "lt quarter panel",
    "rt quarter panel",
    "l quarter panel",
    "r quarter panel",
    "lt quarter outer panel",
    "rt quarter outer panel",
    "l quarter outer panel",
    "r quarter outer panel"
]

FULL_SUGGESTIONS = [
    "adjacent repair rocker panel",
    "adjacent repair rear body",
    "adjacent repair floor",
    "blnd roof rail",
    "blnd rocker panel",
    "r&i liner",
    "r&i qtr glass",
    "r&i roof molding",
    "r&i fuel door (if needed)"
]

ADJACENT_REPAIR_EXCLUSIONS = {
    "adjacent repair rocker panel",
    "adjacent repair rear body",
    "adjacent repair floor"
}

def qtr_panel_rule(lines, seen):
    print("🚀 qtr_panel_rule fired")
    repair_triggered = False
    replacement_triggered = False
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[QTR PANEL RULE] Scanning line: {norm}")

        # 🔍 Repair detection
        if any(qtr in norm for qtr in QTR_IDENTIFIERS) and any(op in norm for op in REPAIR_OPS):
            repair_triggered = True
            print(f"[QTR PANEL RULE] ✅ Repair trigger on line: {lines[i]}")

        # 🔍 CCC-style replacement detection
        if any(qtr in norm for qtr in QTR_IDENTIFIERS) and any(op in norm for op in REPLACE_OPS):
            replacement_triggered = True
            print(f"[QTR PANEL RULE] ✅ CCC-style replacement trigger on line: {lines[i]}")

        # 🔍 Mitchell-style replacement detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and "quarter outer panel" in prev_norm and "/ replace" in norm:
                replacement_triggered = True
                print(f"[QTR PANEL RULE] ✅ Mitchell-style replacement trigger matched at index {i-1}/{i}")

    if not repair_triggered and not replacement_triggered:
        return None

    # 🎯 Dynamic suggestion filtering
    if replacement_triggered:
        suggestions = FULL_SUGGESTIONS
    elif repair_triggered:
        suggestions = [s for s in FULL_SUGGESTIONS if s not in ADJACENT_REPAIR_EXCLUSIONS]
    else:
        suggestions = []

    missing = suggest_if_missing(section_lines, suggestions, seen)
    if missing:
        print(f"[QTR PANEL RULE] 🎯 Suggestions returned: {missing}")
        return ("QUARTER PANEL CHECK", missing)

    return None

def register():
    print("✅ qtr_panel_rule registered")
    return [qtr_panel_rule]
