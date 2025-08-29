import re
from utils import normalize, suggest_if_missing

def rule_grille_adas(line: str, existing_suggestions: list[str]) -> list[str]:
    """
    If the line mentions R&I or Replace + grille/grill, suggest ADAS calibrations.
    """
    norm = normalize(line)

    if any(kw in norm for kw in [
        "r&i", "remove / install", "replace", "repl", "remove/replace"
    ]) and any(part in norm for part in [
        "grille", "grill", "upper grille", "upr grille"
    ]):
        return suggest_if_missing(
            existing_suggestions,
            [
                "360 camera calibration",
                "adaptive cruise control calibration"
            ]
        )
    return []