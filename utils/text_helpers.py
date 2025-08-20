import re

def normalize_lines(lines: list) -> list:
    return [re.sub(r"\s+", " ", line.strip().lower()) for line in lines if line.strip()]

def match_keywords(lines: list, groups: dict) -> dict:
    result = {key: False for key in groups}
    for line in lines:
        for key, keywords in groups.items():
            if any(kw in line for kw in keywords):
                result[key] = True
    return result

def deduplicate(suggestions: list) -> list:
    return list(dict.fromkeys(suggestions))