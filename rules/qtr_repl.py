import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_OPS = ["repl"]
QTR_IDENTIFIERS = ["quarter panel", "quarter outer panel"]

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

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[QTR REPL RULE] Scanning line: {norm}")

        # 🔍 Standard CCC-style detection
        if any(part in norm for part in QTR_IDENTIFIERS) and any(op in norm for op in REPLACE_OPS):
            triggered = True
            print(f"[QTR REPL RULE] ✅ Standard trigger on line: {lines[i]}")
            break

        # 🔍 Mitchell-style pairing detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and any(part in prev_norm for part in QTR_IDENTIFIERS) and "/ replace" in norm:
                mitchell_triggered = True
                print(f"[QTR REPL RULE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")
                break

    if not triggered and not mitchell_triggered:
        return None

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[QTR REPL RULE] 🎯 Suggestions returned: {missing}")
        return ("QUARTER PANEL MATERIAL CHECK", missing)

    return None

def register():
    print("✅ qtr_repl_rule registered")
    return [qtr_repl_rule]