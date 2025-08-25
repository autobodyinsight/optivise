def bumper_repair_suggestions(text: str, tags: set, section: str) -> tuple:
    text_lower = text.lower()

    repair_terms = {"rpr", "repair"}
    bumper_terms = {"bumper", "bumper cover", "fascia", "facebar", "face bar"}

    if any(r in text_lower for r in repair_terms) and any(b in text_lower for b in bumper_terms):
        return (
            "bumper_repair",
            [{
                "category": "bumper",
                "summary": "Check bumper repair logic",
                "detail": f"Line mentions repair and bumper: '{text}'",
                "tags": ["bumper", "repair"]
            }]
        )
    return None

def register():
    return [bumper_repair_suggestions]