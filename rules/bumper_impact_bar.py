import re
from utils import normalize

OPS = ["repl", "replace", "remove / replace", "rem / repl"]
PARTS = ["impact bar", "rebar", "reinforcement beam", "reinforcement", "bumper beam"]
HEADERS = ["FRONT BUMPER", "REAR BUMPER"]

SUGGESTIONS = [
    "VERIFY if refinish is required",
    "ADD for 2nd color tint (if rebar is not the same color of car)"
]

def impact_bar_rule(lines, seen):
    in_bumper_section = False
    found_match = False
    paint_present = False

    for line in lines:
        norm = normalize_operation(normalize_orientation(line))

        # Detect section entry: line contains a known bumper header
        if any(h in line for h in HEADERS):
            in_bumper_section = True
            print(f"[IMPACT BAR RULE] Entered section: {line.strip()}")
            continue

        # Exit section: any new all-caps header not in HEADERS
        if re.match(r"^[A-Z ]{5,}$", line.strip()) and not any(h in line for h in HEADERS):
            in_bumper_section = False

        if in_bumper_section:
            # Detect paint labor
            if ("paint" in norm or "refinish" in norm) and re.search(r"\d+(\.\d+)?", norm):
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
            return ("BUMPER IMPACT BAR REFINISH CHECK", suggestions)

    return None

def register():
    return [impact_bar_rule]