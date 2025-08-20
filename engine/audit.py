from rules.bumper import evaluate_bumper
from utils.text_helpers import normalize_lines

def run_audit(pdf_lines: list) -> dict:
    normalized = normalize_lines(pdf_lines)
    bumper_suggestions = evaluate_bumper(normalized)
    return {
        "bumper": bumper_suggestions
    }