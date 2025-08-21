# app/utils.py

def normalize(text: str) -> str:
    """Normalize text for consistent rule matching."""
    return text.strip().lower().replace('\n', ' ').replace('\r', '')