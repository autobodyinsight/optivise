import re

def normalize(text):
    return re.sub(r'[^a-z0-9\s]', '', text.lower())

def contains_all_keywords(line, keywords):
    norm_line = normalize(line)
    return all(re.search(rf'\b{kw}\b', norm_line) for kw in keywords)

def rule_fender_accessory_check(estimate_lines):
    trigger_keywords = [["rpr", "repair", "rep"], ["fender", "fndr"]]
    required_accessories = [
        ["r&i", "fender", "liner"],
        ["r&i", "wheel", "opng", "mldg"],
        ["r&i", "mud", "guard"],
        ["r&i", "corner", "molding"],
        ["r&i", "rocker", "molding"]
    ]

    normalized_lines = [normalize(line) for line in estimate_lines]

    # 🔍 Check if any line contains both trigger keyword groups
    triggered = any(
        contains_all_keywords(line, trigger_keywords[0]) and
        contains_all_keywords(line, trigger_keywords[1])
        for line in normalized_lines
    )

    if not triggered:
        return []

    # 🧠 Suggest missing accessories
    suggestions = []
    for accessory in required_accessories:
        found = any(contains_all_keywords(line, accessory) for line in normalized_lines)
        if not found:
            suggestions.append("rá " + " ".join(accessory))

    return suggestions