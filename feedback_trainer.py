import json
import os

FEEDBACK_FILE = "feedback_log.json"

def log_feedback(pdf_id: str, missed_item: str, context_lines: list):
    """Store feedback for missed suggestions."""
    feedback = {
        "pdf_id": pdf_id,
        "missed_item": missed_item,
        "context_lines": context_lines
    }

    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([feedback], f, indent=2)
    else:
        with open(FEEDBACK_FILE, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(feedback)
            f.seek(0)
            json.dump(data, f, indent=2)

def get_learned_patterns():
    """Return learned patterns from feedback."""
    if not os.path.exists(FEEDBACK_FILE):
        return []

    with open(FEEDBACK_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []

    patterns = set()
    for entry in data:
        for line in entry.get("context_lines", []):
            if entry["missed_item"].lower() in line.lower():
                patterns.add(line.strip().lower())

    return list(patterns)