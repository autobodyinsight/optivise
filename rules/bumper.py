def bumper_rule(line, seen):
    suggestions = []

    # Normalize line
    normalized = line.lower()

    # Determine bumper type
    is_front = "front bumper" in normalized
    is_rear = "rear bumper" in normalized
    is_ambiguous = "bumper" in normalized and not (is_front or is_rear)

    # Front bumper logic
    if is_front or is_ambiguous:
        if "repair" in normalized and "cover" in normalized:
            if "flex additive" not in seen:
                suggestions.append("flex additive")
                seen.add("flex additive")
        if "replace" in normalized:
            if "bumper cover" not in seen:
                suggestions.append("bumper cover")
                seen.add("bumper cover")

    # Rear bumper logic
    if is_rear or is_ambiguous:
        if "repair" in normalized and "cover" in normalized:
            if "refinish rear bumper" not in seen:
                suggestions.append("refinish rear bumper")
                seen.add("refinish rear bumper")
        if "replace" in normalized:
            if "rear bumper cover" not in seen:
                suggestions.append("rear bumper cover")
                seen.add("rear bumper cover")

    return suggestions