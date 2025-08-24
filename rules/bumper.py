from utils.rules_engine import Rule, Suggestion
from utils.line_tools import normalize_line

def bumper_repair_suggestions(lines):
    suggestions = []
    bumper_repair_detected = False
    current_category = None

    bumper_keywords = {"FRONT BUMPER", "FRONT BUMPER & GRILLE", "REAR BUMPER"}

    for line in lines:
        norm = normalize_line(line)

        # Detect category headers
        if norm in bumper_keywords:
            current_category = norm
            continue

        # Detect bumper repair operation
        if current_category and "rpr bumper" in norm:
            bumper_repair_detected = True

    if bumper_repair_detected:
        suggestions.extend([
            Suggestion("Add flex additive"),
            Suggestion("Add bumper repair kit"),
            Suggestion("Add static neutralization")
        ])

    return Rule(
        name="bumper_repair_suggestions",
        condition="Detects bumper repair in front or rear",
        suggestions=suggestions
    )