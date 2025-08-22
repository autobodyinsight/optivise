def normalize(text: str) -> str:
    """Normalize text for consistent rule matching."""
    return text.strip().lower().replace('\n', ' ').replace('\r', '')

def suggest_if_missing(lines: list, candidates: list, seen: set) -> list:
    """
    Returns items from candidates that aren't already present in any line.
    Uses token containment instead of exact match.
    """
    normalized_lines = [normalize(line) for line in lines]
    return [
        item for item in candidates
        if not any(normalize(item) in line for line in normalized_lines)
    ]