def normalize(text: str) -> str:
    """Normalize text for consistent rule matching."""
    return text.strip().lower().replace('\n', ' ').replace('\r', '')

def suggest_if_missing(lines: list, candidates: list, seen: set) -> list:
    """
    Returns items from candidates that aren't already in seen.
    Assumes 'seen' contains normalized strings.
    """
    return [item for item in candidates if normalize(item) not in seen]