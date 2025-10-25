import re
from utils import normalize, normalize_orientation, normalize_operation

REPAIR_OPS = ["rpr", "repair", "rep"]
REPLACE_OPS = ["replace", "repl", "remove / replace", "lkq", "assy"]

QTR_IDENTIFIERS = [
    "quarter panel", "quarter outer panel", "quarter pnl",
    "lt quarter panel", "rt quarter panel", "l quarter panel", "r quarter panel",
    "lt quarter outer panel", "rt quarter outer panel", "l quarter outer panel", "r quarter outer panel"
]

ADJACENT_REPAIR_EXCLUSIONS = {
    "adjacent repair rocker panel",
    "adjacent repair rear body",
    "adjacent repair floor"
}

# Canonical suggestions
SUGGESTIONS = {
    "adjacent repair rocker panel": ["adjacent repair rocker panel"],
    "adjacent repair rear body": ["adjacent repair rear body"],
    "adjacent repair floor": ["adjacent repair floor"],
    "blnd roof rail": ["blend roof rail", "blnd roof rail"],
    "blnd rocker panel": ["blend rocker panel", "blnd rocker panel"],
    "r&i liner": ["liner", "splash shield"],
    "r&i quarter glass": ["quarter glass", "qtr glass"],
    "r&i roof molding": ["roof molding", "roof w'strip"],
    "r&i fuel door (if needed)": ["fuel door"]
}

def qtr_panel_rule(lines, seen):
    print("🚀 qtr_panel_rule fired")
    repair_triggered = False
    replacement_triggered = False

    normalized_seen = set(normalize(item) for item in seen)

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        print(f"[QTR PANEL RULE] Scanning line: {norm}")

        if any(qtr in norm for qtr in QTR_IDENTIFIERS):
            if any(op in norm for op in REPAIR_OPS):
                repair_triggered = True
                print(f"[QTR PANEL RULE] ✅ Repair trigger on line: {lines[i]}")
            if any(op in norm for op in REPLACE_OPS):
                replacement_triggered = True
                print(f"[QTR PANEL RULE] ✅ CCC-style replacement trigger on line: {lines[i]}")

        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and "quarter outer panel" in prev_norm and "/ replace" in norm:
                replacement_triggered = True
                print(f"[QTR PANEL RULE] ✅ Mitchell-style replacement trigger matched at index {i-1}/{i}")

    if not repair_triggered and not replacement_triggered:
        return None

    # Filter suggestions based on trigger type
    if replacement_triggered:
        active_suggestions = list(SUGGESTIONS.keys())
    elif repair_triggered:
        active_suggestions = [s for s in SUGGESTIONS if s not in ADJACENT_REPAIR_EXCLUSIONS]
    else:
        active_suggestions = []

    # Scan for missing items
    missing = []
    for label in active_suggestions:
        aliases = SUGGESTIONS[label]
        found = any(
            any(re.search(rf"\b{normalize(alias)}\b", normalize(line)) for alias in aliases)
            for line in lines
        )
        if not found and normalize(label) not in normalized_seen:
            missing.append(label)

    if missing:
        print(f"[QTR PANEL RULE] 🎯 Suggestions returned: {missing}")
        return ("QUARTER PANEL CHECK", missing)

    return None

def register():
    print("✅ qtr_panel_rule registered")
    return [qtr_panel_rule]