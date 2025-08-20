from utils.text_helpers import match_keywords, deduplicate

KEYWORD_GROUPS = {
    "replace": ["replace", "remove", "install"],
    "repair": ["repair", "refinish", "straighten"],
    "bumper": ["bumper", "cover", "fascia"]
}

SUGGESTIONS = {
    "replace": "Consider replacing the front bumper if damage is extensive.",
    "repair": "Repair may be sufficient for minor bumper damage.",
}

def evaluate_bumper(lines: list) -> list:
    matched = match_keywords(lines, KEYWORD_GROUPS)
    suggestions = []

    if matched["replace"] and matched["bumper"]:
        suggestions.append(SUGGESTIONS["replace"])
    elif matched["repair"] and matched["bumper"]:
        suggestions.append(SUGGESTIONS["repair"])

    return deduplicate(suggestions)