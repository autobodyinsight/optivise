import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_OPS = ["repl"]
QTR_IDENTIFIERS = [
    "quarter panel",
    "quarter outer panel",
    "lt quarter panel",
    "rt quarter panel",
    "l quarter panel",
    "r quarter panel",
    "lt quarter outer panel",
    "rt quarter outer panel",
    "l quarter outer panel",
    "r quarter outer panel"
]

SUGGESTIONS = [
    "weldthrough primer",
    "weld through primer",
    "panel bond",
    "bonding foam",
    "sound deadening",
    "seam sealer",
    "cavity wax",
    "corrosion protection"
]

def qtr_repl_rule(lines, seen):
    print("🚀 qtr_repl_rule fired")
    triggered = False
    mitchell_triggered = False
    section_lines = []

    trigger_index = None

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[QTR REPL RULE] Scanning line: {norm}")

        # 🔍 Standard CCC-style detection
        if any(part in norm for part in QTR_IDENTIFIERS) and any(op in norm for op in REPLACE_OPS):
            triggered = True
            trigger_index = i
            print(f"[QTR REPL RULE] ✅ Standard trigger on line: {lines[i]}")
            break

        # 🔍 Mitchell-style pairing detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and any(part in prev_norm for part in QTR_IDENTIFIERS) and "/ replace" in norm:
                mitchell_triggered = True
                trigger_index = i
                print(f"[QTR REPL RULE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")
                break

    if not triggered and not mitchell_triggered:
        return None

    # 🔁 Continue collecting lines after trigger for