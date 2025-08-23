# rules/rear_bumper.py

from utils.matching import keyword_in_line, has_any_keywords

CATEGORY_HEADER = "REAR BUMPER"

REQUIRED_SUGGESTIONS = [
    "Flex additive",
    "Bumper repair kit",
    "Mask for texture",
    "Mask for two tone",
    "ADD for parking sensors",
    "ADD R&I tail lights"
]

TEXTURE_KEYWORDS = ["texture", "textured"]
TWO_TONE_KEYWORDS = ["two tone", "2-tone"]
PARK_SENSOR_KEYWORDS = ["sensor", "park sensor", "parking sensor"]
TAIL_LIGHT_KEYWORDS = ["tail light", "taillight", "R&I tail light"]

def normalize(text):
    return text.lower().strip()

def analyze_rear_bumper(lines):
    suggestions = []
    in_rear_bumper = False
    found_items = set(normalize(line) for line in lines if line.strip())

    for line in lines:
        line_lower = normalize(line)

        if CATEGORY_HEADER.lower() in line_lower:
            in_rear_bumper = True
            continue

        if in_rear_bumper and line.strip() == "":
            break  # End of category block

        if in_rear_bumper:
            # Detect texture or two-tone
            if has_any_keywords(line_lower, TEXTURE_KEYWORDS):
                if normalize("Mask for texture") not in found_items:
                    suggestions.append("Mask for texture")

            if has_any_keywords(line_lower, TWO_TONE_KEYWORDS):
                if normalize("Mask for two tone") not in found_items:
                    suggestions.append("Mask for two tone")

            if has_any_keywords(line_lower, PARK_SENSOR_KEYWORDS):
                if normalize("ADD for parking sensors") not in found_items:
                    suggestions.append("ADD for parking sensors")

            if has_any_keywords(line_lower, TAIL_LIGHT_KEYWORDS):
                if normalize("ADD R&I tail lights") not in found_items:
                    suggestions.append("ADD R&I tail lights")

    # Add default suggestions only if not already present
    for item in REQUIRED_SUGGESTIONS:
        if normalize(item) not in found_items and item not in suggestions:
            suggestions.append(item)

    return suggestions