import re
from utils import normalize, suggest_if_missing

# 🔧 Material items to suggest
MATERIAL_ITEMS = {
    "outer panel": [
        "weldthrough primer", "weld through primer", "cavity wax", "corrosion protection",
        "bonding foam", "anti flutter foam", "sound deadening pad", "panel bond"
    ],
    "quarter panel": [
        "weldthrough primer", "weld through primer", "cavity wax", "corrosion protection",
        "bonding foam", "anti flutter foam", "sound deadening pad", "seam sealer", "panel bond"
    ],
    "floor pan": [
        "weldthrough primer", "weld through primer", "cavity wax", "corrosion protection",
        "bonding foam", "anti flutter foam", "sound deadening pad", "seam sealer", "panel bond"
    ],
    "rear body panel": [
        "weldthrough primer", "weld through primer", "cavity wax", "corrosion protection",
        "seam sealer", "panel bond"
    ]
}

# 🔍 Match triggers
REPLACE_TRIGGERS = ["repl", "replace", "/replace"]
REMOVE_TRIGGERS = ["remove"]
COMPONENT_TRIGGERS = {
    "outer panel": ["outer panel", "door repair panel"],
    "quarter panel": ["quarter panel", "quarter outer panel"],
    "floor pan": ["floor pan", "rear body floor pan"],
    "rear body panel": ["rear body panel"]
}

def materials_rule(lines, seen):
    suggestions = []
    normalized_lines = [normalize(line) for line in lines]

    for idx, norm in enumerate(normalized_lines):
        # 🔍 Check direct replacement line
        for component, aliases in COMPONENT_TRIGGERS.items():
            if any(rep in norm for rep in REPLACE_TRIGGERS) and any(alias in norm for alias in aliases):
                print(f"[MATERIALS] ✅ Direct replacement detected: {lines[idx]}")
                suggestions += missing_materials(lines, component, seen)
                break

        # 🔍 Check Mitchell-style: /replace + line above has remove + component
        if any(rep in norm for rep in REPLACE_TRIGGERS) and idx > 0:
            prev = normalized_lines[idx - 1]
            for component, aliases in COMPONENT_TRIGGERS.items():
                if any(rem in prev for rem in REMOVE_TRIGGERS) and any(alias in prev for alias in aliases):
                    print(f"[MATERIALS] ✅ Mitchell-style replacement detected:\n→ {lines[idx - 1]}\n→ {lines[idx]}")
                    suggestions += missing_materials(lines, component, seen)
                    break

    if suggestions:
        return ("MATERIALS & REFINISH CHECK", suggestions)
    return None

# 🧠 Check for missing refinishing materials
def missing_materials(lines, component, seen):
    required = MATERIAL_ITEMS[component]
    found = set()

    for line in lines:
        norm = normalize(line)
        for item in required:
            if item in norm:
                found.add(item)

    missing = [item for item in required if item not in found and item not in seen]
    print(f"[MATERIALS] 🎯 Missing for '{component}': {missing}")
    return missing

def register():
    return [materials_rule]
