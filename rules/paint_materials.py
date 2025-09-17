import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

TRIGGER_TERMS = ["body labor", "paint labor"]

SUGGESTIONS = [
    "cover car",
    "cover car for primer",
    "mask jambs (if repair or replace to rad supp, rear body, floor, ctr pillar, or rocker panel)",
    "gravel guard (if present)",
    "tint",
    "spray out",
    "colorsand and buff (to match finish texture)",
    "denib and polish (to remove dirt nibs)",
    "mask wshield (if blending roof rail)",
    "mask backglass(if quarter repair)",
    "blend roof rail"
]

# Synonym normalization for paint material terms
def normalize_material(term):
    term = term.lower().strip()
    synonyms = {
        "cover car": {"mask for overspray"},
        "cover car for primer": {"mask for primer"},
    }
    for canonical, variants in synonyms.items():
        if term == canonical or term in variants:
            return canonical
    return term

def paint_materials_rule(lines, seen):
    print("🚀 paint_materials_rule fired")
    triggered = False
    section_lines = []

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))
        section_lines.append(line)

        if any(term in norm for term in TRIGGER_TERMS):
            triggered = True
            print(f"[PAINT MATERIALS RULE] ✅ Triggered on line: {line}")
            break

    if not triggered:
        return None

    notes = " ".join(lines).lower()
    if "roof rail blend" in notes or "blend roof rail" in notes:
        SUGGESTIONS.extend(["mask wshield", "mask backglass", "blend roof rail"])
    if "quarter repair" in notes:
        SUGGESTIONS.extend(["mask backglass", "blend roof rail"])

    normalized_seen = {normalize_material(item) for item in seen}
    missing = suggest_if_missing(section_lines, SUGGESTIONS, normalized_seen)

    if missing:
        print(f"[PAINT MATERIALS RULE] 🎯 Suggestions returned: {missing}")
        return ("PAINT MATERIALS CHECK", missing)

    return None

def register():
    print("✅ paint_materials_rule registered")
    return [paint_materials_rule]
