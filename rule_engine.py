import importlib
import pkgutil
import rules
from utils import normalize

def load_rules():
    """Dynamically loads all rule functions from app.rules modules."""
    rule_funcs = []
    for _, module_name, _ in pkgutil.iter_modules(rules.__path__):
        module = importlib.import_module(f"rules.{module_name}")
        if hasattr(module, "register"):
            rule_funcs.extend(module.register())
    return rule_funcs

def run_rules(parsed_data: dict) -> list:
    """
    Applies all registered audit rules to parsed estimate data.
    """
    lines = parsed_data.get("raw_lines", [])
    seen = set(normalize(line) for line in lines)

    results = []
    rules = load_rules()

    for rule in rules:
        result = rule(lines, seen)
        print(f"🛠️ Rule {rule.__name__} result:", result)  # Debug print

        if result:
            rule_name, suggestions = result
            results.append({
                "rule": rule_name,
                "suggestions": suggestions
            })

    return results