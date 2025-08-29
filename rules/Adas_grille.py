from utils.matching import contains_any, normalize_line
from utils.suggestions import suggest_if_missing

def rule_grille_adas(line: str, existing_suggestions: list[str]) -> list[str]:
    """
    If the line mentions R&I or Replace + grille/grill, suggest ADAS calibrations.
    """
    norm = normalize_line(line)

    action_keywords = ["r&i", "remove", "install", "replace", "rpl", "repl"]
    part_keywords = ["grille", "grill"]

    if contains_any(norm, action_keywords) and contains_any(norm, part_keywords):
        return suggest_if_missing(
            existing_suggestions,
            [
                "360 camera calibration",
                "adaptive cruise control calibration"
            ]
        )
    return []