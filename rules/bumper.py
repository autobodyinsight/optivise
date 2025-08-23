from utils import normalize

def bumper_rule(line, seen, context):
    suggestions = []
    normalized = normalize(line)

    print(f"[bumper_rule] Context: {context} | Line: {line}")

    verbs = ["repair", "r&i", "replace", "remove", "install", "refinish"]
    parts = ["bumper", "cover", "fascia", "bumper assy", "facebar", "face bar"]

    if context == "front":
        if any(v in normalized for v in verbs) and any(p in normalized for p in parts):
            if "flex additive" not in seen:
                suggestions.append("flex additive")
                seen.add("flex additive")

    elif context == "rear":
        if any(v in normalized for v in verbs) and any(p in normalized for p in parts):
            if "refinish rear bumper" not in seen:
                suggestions.append("refinish rear bumper")
                seen.add("refinish rear bumper")

    return suggestions

def register():
    return [lambda line, seen, context: ("bumper_rule", bumper_rule(line, seen, context))]