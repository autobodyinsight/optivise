import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_OPS = ["repl"]
MATERIAL_IDENTIFIERS = [
    "lt outer panel", "rt outer panel",
    "lt quarter panel", "rt quarter panel",
    "floor pan", "rear body panel"
]

MITCHELL_IDENTIFIERS = [
    "frt door repair panel",
    "lt door repair panel", "rt door repair panel",
    "l door repair panel", "r door repair panel",
    "front door repair panel", "rear door repair panel",
    "quarter outer panel",
    "rear body panel",
    "rear body floor pan"
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

def materials_rule(lines, seen):
    print("🚀 materials_rule fired")
    triggered_identifiers = []
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[MATERIALS RULE] Scanning line: {norm}")

        # 🔍 Mitchell-style detection first
        if "/ replace" in norm and i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm:
                for identifier in MITCHELL_IDENTIFIERS:
                    if normalize(identifier) in prev_norm:
                        upper_id = identifier.upper()
                        if upper_id not in triggered_identifiers:
                            triggered_identifiers.append(upper_id)
                            print(f"[MATERIALS RULE] ✅ Mitchell-style trigger: {upper_id} at index {i-1}/{i}")
                        break
            continue

        # 🔍 CCC-style detection
        for identifier in MATERIAL_IDENTIFIERS:
            if identifier in norm and any(op in norm for op in REPLACE_OPS):
                upper_id = identifier.upper()
                if upper_id not in triggered_identifiers:
                    triggered_identifiers.append(upper_id)
                    print(f"[MATERIALS RULE] ✅ CCC-style trigger: {upper_id} on line: {lines[i]}")
                break

    if not triggered_identifiers:
        return None

    missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
    if missing:
        print(f"[MATERIALS RULE] 🎯 Triggered identifiers (ordered): {triggered_identifiers}")
        print(f"[MATERIALS RULE] 🎯 Suggestions returned: {missing}")
        return ("MATERIALS CHECK", triggered_identifiers + missing)

    return None

def register():
    print("✅ materials_rule registered")
    return [materials_rule]
