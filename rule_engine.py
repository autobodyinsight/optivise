import importlib
import pkgutil
import rules
from utils import normalize
from rules.vehicle_identifier import vehicle_identifier_rule  # ✅ Import vehicle rule explicitly

def load_rules():
    """Dynamically loads all rule functions from rules modules."""
    rule_funcs = []
    for _, module_name, _ in pkgutil.iter_modules(rules.__path__):
        if module_name != "vehicle_identifier":  # ✅ Skip vehicle rule here (run it manually)
            module = importlib.import_module(f"rules.{module_name}")
            if hasattr(module, "register"):
                rule_funcs.extend(module.register())
    return rule_funcs

def run_rules(parsed_data: dict) -> list:
    """
    Applies all registered audit rules to parsed estimate data,
    ensuring suggestions are not duplicated across rules.
    """
    lines = parsed_data.get("raw_lines", [])
    seen_lines = set(normalize(line) for line in lines)
    seen_suggestions = set()

    results = []

    # ✅ Run vehicle identifier rule first
    vehicle_result = vehicle_identifier_rule(lines, seen_lines)
    if vehicle_result:
        rule_name, suggestions = vehicle_result
        deduped = [s for s in suggestions if normalize(s) not in seen_suggestions]
        seen_suggestions.update(normalize(s) for s in deduped)

        if deduped:
            results.append({
                "rule": rule_name,
                "suggestions": deduped
            })

    # 🔁 Load and run all other rules
    rules = load_rules()
    for rule in rules:
        result = rule(lines, seen_lines | seen_suggestions)
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