import re
from utils import normalize, sectionize

OPS = ["repl", "replace", "remove / replace", "rem / repl"]
PARTS = ["impact bar", "rebar", "reinforcement beam", "reinforcement", "bumper beam"]
HEADERS = ["FRONT BUMPER", "REAR BUMPER"]

SUGGESTIONS = [
    "VERIFY if refinish is required",
    "ADD for 2nd color tint (if rebar is not the same color of car)"
]

def impact_bar_rule(lines, seen):
    sections = sectionize(lines)
    for header, content in sections.items():
        if header not in HEADERS:
            continue

        print(f"[IMPACT BAR RULE] Scanning section: {header}")
        found_match = False
        paint_present = False

        for line in content:
            norm = normalize(line)

            # Detect paint labor
            if re.search(r"\bpaint\b", norm) and re.search(r"\d+(\.\d+)?", norm):
                paint_present = True

            # Detect operation + part adjacency
            for op in OPS:
                for part in PARTS:
                    pattern = rf"\b{op}\b.*\b{part}\b|\b{part}\b.*\b{op}\b"
                    if re.search(pattern, norm):
                        print(f"[IMPACT BAR RULE] Match found: {line}")
                        found_match = True

        if found_match and not paint_present:
            suggestions = [s for s in SUGGESTIONS if s not in seen]
            if suggestions:
                return (f"{header} IMPACT BAR REFINISH CHECK", suggestions)

    return None

def register():
    return [impact_bar_rule]