import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

def rule_grille_adas(lines: list[str], seen: set[str]) -> tuple[str, list[str]] | None:
    """
    If any line mentions grille replacement or R&I, suggest ADAS calibrations.
    Includes Mitchell-style detection: / replace or / install paired with 'remove' + 'grille' on the line above.
    """
    action_keywords = ["r&i", "remove / install", "replace", "repl", "remove/replace"]
    grille_keywords = ["grille", "grill"]
    mitchell_triggered = False

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))

        # 🔍 Standard detection
        if any(kw in norm for kw in action_keywords) and any(part in norm for part in grille_keywords):
            suggestions = suggest_if_missing(
                lines,
                [
                    "360 camera calibration (if equipped)",
                    "adaptive cruise control calibration (if equipped)"
                ],
                seen
            )
            if suggestions:
                print(f"[ADAS GRILLE] ✅ Standard match on line: {lines[i]}")
                return ("ADAS GRILLE CHECK", suggestions)

        # 🔍 Mitchell-style trigger detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if ("remove" in prev_norm and any(part in prev_norm for part in grille_keywords)) and ("/ replace" in norm or "/ install" in norm):
                mitchell_triggered = True
                print(f"[ADAS GRILLE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")

    if mitchell_triggered:
        suggestions = suggest_if_missing(
            lines,
            [
                "360 camera calibration (if equipped)",
                "adaptive cruise control calibration (if equipped)"
            ],
            seen
        )
        if suggestions:
            print(f"[ADAS GRILLE] ✅ Triggered by Mitchell-style pairing")
            return ("ADAS GRILLE CHECK", suggestions)

    return None

def register():
    return [rule_grille_adas]