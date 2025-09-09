from utils import suggest_if_missing

MATERIAL_MAP = {
    "BUMPER REPAIR CHECK": [
        "flex additive",
        "adhesion promoter",
        "bumper repair kit"
    ],
    "FENDER REPAIR CHECK": [
        "corrosion protection",
        "feather prime and block",
        "gravel guard (if needed)",
        "bonding foam",
        "bonding foam removal",
        "backside refinish (if required)"
    ],
    "FLOOR PAN REPLACEMENT CHECK": [
        "corrosion protection",
        "undercoating",
        "panel bond (if needed)",
        "seam sealer",
        "sound deadening pads (if needed)",
        "weldthrough primer",
        "weld through primer",
        "cavity wax"
    ],
    "FRONT BUMPER REPLACEMENT CHECK": [
        "adhesion promoter",
        "flex additive"
    ],
    "QUARTER PANEL REPAIR CHECK": [
        "weldthrough primer",
        "weld through primer",
        "seam sealer",
        "sound deadening pad (if needed)",
        "undercoating",
        "corrosion protection",
        "panel bond (if needed)",
        "bonding foam"
    ],
    "REAR BUMPER REPAIR CHECK": [
        "flex additive",
        "adhesion promoter",
        "bumper repair kit"
    ],
    "REAR BODY + FLOOR REPAIR CHECK": [
        "corrosion protection",
        "sound deadening pad (if needed)",
        "seam sealer (if needed)"
    ],
    "REAR BODY PANEL REPLACEMENT CHECK": [
        "weldthrough primer",
        "weld through primer",
        "seam sealer",
        "corrosion protection",
        "sound deadening pad",
        "panel bond"
    ]
}

def repair_materials_rule(lines, seen):
    print("🚀 repair_materials_rule fired")
    section_lines = lines  # Use full estimate context

    all_suggestions = []
    for rule_label, materials in MATERIAL_MAP.items():
        if rule_label in seen:
            print(f"[REPAIR MATERIALS] ✅ Rule triggered: {rule_label}")
            missing = suggest_if_missing(section_lines, materials, seen)
            if missing:
                print(f"[REPAIR MATERIALS] 🎯 Suggestions for {rule_label}: {missing}")
                all_suggestions.extend(missing)

    if all_suggestions:
        return ("REPAIR MATERIALS CHECK", sorted(set(all_suggestions)))

    return None

def register():
    print("✅ repair_materials_rule registered")
    return [repair_materials_rule]