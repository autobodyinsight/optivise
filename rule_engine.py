import importlib
import pkgutil
import rules
from utils import normalize

class Suggestion:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Suggestion({self.text!r})"


class Rule:
    def __init__(self, name: str, condition: str, suggestions: list):
        self.name = name
        self.condition = condition
        self.suggestions = suggestions

    def __str__(self):
        return f"{self.name}: {self.condition}"

    def __repr__(self):
        return f"Rule({self.name!r}, {self.condition!r}, {self.suggestions!r})"

def load_rules():
    """Dynamically loads all rule functions from rules modules."""
    rule_funcs = []
    for _, module_name, _ in pkgutil.iter_modules(rules.__path__):
        module = importlib.import_module(f"rules.{module_name}")
        if hasattr(module, "register"):
            rule_funcs.extend(module.register())
    return rule_funcs

def run_rules(parsed_data: dict) -> list:
    """
    Applies all registered audit rules to parsed estimate data,
    using section context from bold headers and ensuring suggestions are deduplicated.
    """
    lines = parsed_data.get("raw_lines", [])
    seen_suggestions = set()
    results = []

    current_section = None
    rule_funcs = load_rules()

    for line_obj in lines:
        text = line_obj["text"]
        is_bold = line_obj.get("is_bold", False)

        # Track section context from bold headers
        if is_bold:
            lowered = text.lower()
            if "front bumper" in lowered:
                current_section = "front"
            elif "rear bumper" in lowered:
                current_section = "rear"
            else:
                current_section = None
            continue  # skip bold line itself

        for rule in rule_funcs:
            result = rule(text, seen_suggestions, current_section)
            if result:
                rule_name, suggestions = result
                deduped = [s for s in suggestions if normalize(s) not in seen_suggestions]
                seen_suggestions.update(normalize(s) for s in deduped)

                if deduped:
                    results.append({
                        "rule": rule_name,
                        "suggestions": deduped
                    })

    return results

if __name__ == "__main__":
    lines = ["Repair front bumper cover"]
    seen = set()

    from rules.bumper import bumper_rule

    print("Front bumper result:", bumper_rule(lines, seen))