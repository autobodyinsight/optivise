from utils import normalize
from rule_engine import Rule, Suggestion

def bumper_repair_suggestions(text, seen_suggestions, current_section):
    norm = normalize(text)
    suggestions = []

    # Only run if we're inside a bumper section
    if current_section in {"front", "rear"} and "rpr bumper" in norm:
        suggestions.extend([
            "Add flex additive",
            "Add bumper repair kit",
            "Add static neutralization"
        ])

    return ("bumper_repair_suggestions", suggestions) if suggestions else None

def register():
    return [bumper_repair_suggestions]