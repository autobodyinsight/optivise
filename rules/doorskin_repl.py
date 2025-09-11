import re
from utils import normalize, normalize_orientation, normalize_operation

REPLACEMENT_OPS = ["replace", "repl"]
DOOR_SKIN_IDENTIFIERS = ["outer panel", "frt door repair panel"]

SUGGESTED_MATERIALS = [
    "weldthrough primer",
    "weld through primer",
    "panel bond",
    "bonding foam",
    "sound deadening",
    "seam sealer",
    "cavity wax",
    "corrosion protection"
]

def doorskin_repl_rule(lines, seen):
    triggered = False
    mitchell_triggered = False
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])

        # 🔍 Standard CCC-style detection
        if any(idf in norm for idf in DOOR_SKIN_IDENTIFIERS):
            if any(op in norm for op in REPLACEMENT_OPS) or "repl lt outer panel" in norm:
                triggered = True
                print(f"[DOORSKIN REPL] ✅ Standard trigger on line: {lines[i]}")
                break

        # 🔍 Mitchell-style pairing detection (remove + frt door repair panel / replace)
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and "frt door repair panel" in prev_norm:
                if "/ replace" in norm:
                    mitchell_triggered = True
                    print(f"[DOORSKIN REPL] ✅ Mitchell-style trigger matched at index {i-1}/{i}")
                    break

    if not triggered and not mitchell_triggered:
        return None

    missing_materials = []
    for material in SUGGESTED_MATERIALS:
        present = any(re.search(rf"\b{normalize(material)}\b", normalize(line)) for line in section_lines)
        if not present and material not in seen:
            missing_materials.append(material)

    if missing_materials:
        print(f"[DOORSKIN REPL] 🎯 Suggestions returned: {missing_materials}")
        return ("DOORSKIN MATERIAL CHECK", missing_materials)

    return None

def register():
    print("✅ doorskin_repl_rule registered")
    return [doorskin_repl_rule]