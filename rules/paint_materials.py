import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

def materials_rule(estimate):
    body_labor = estimate.get("body_labor", 0)
    paint_labor = estimate.get("paint_labor", 0)
    notes = estimate.get("notes", "").lower()
    existing_ops = {normalize(op) for op in estimate.get("operations", [])}

    if body_labor + paint_labor == 0:
        return []

    suggestions = []

    # Always-suggested operations
    suggestions += suggest_if_missing(existing_ops, "cover car", "Required for primer masking")
    suggestions += suggest_if_missing(existing_ops, "mask jambs", "Applicable if jambs are being refinished")
    suggestions += suggest_if_missing(existing_ops, "gravel guard", "Applicable if lower panels need protection")
    suggestions += suggest_if_missing(existing_ops, "tint", "Needed for blendable color match")
    suggestions += suggest_if_missing(existing_ops, "spray out", "Required for 3-stage color match")
    suggestions += suggest_if_missing(existing_ops, "colorsand and buff", "Recommended: 0.5 hrs per panel")
    suggestions += suggest_if_missing(existing_ops, "denib and polish", "Final finish enhancement")

    # Conditional triggers
    if re.search(r"roof rail blend|blend roof rail", notes) or "blend roof rail" in existing_ops:
        suggestions += suggest_if_missing(existing_ops, "mask wshield", "Windshield masking needed for roof rail blend")
        suggestions += suggest_if_missing(existing_ops, "mask backglass", "Backglass masking needed for roof rail blend")

    if "quarter repair" in notes:
        suggestions += suggest_if_missing(existing_ops, "mask backglass", "Backglass masking needed for quarter repair")
        suggestions += suggest_if_missing(existing_ops, "blend roof rail", "Clear coat required on roof rail for quarter repair")

    return suggestions

def register():
    print("✅ materials_rule registered")
    return [materials_rule]
