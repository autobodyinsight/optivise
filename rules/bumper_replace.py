import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_PHRASES = [
    "repl bumper", "replace bumper",
    "repl bumper cover", "replace bumper cover",
    "repl fascia", "replace fascia",
    "repl bumper cover assy", "replace bumper cover assy",
    "repl bumper cover assembly", "replace bumper cover assembly"
]

GENERIC_BUMPER_TERMS = ["upper cover", "fascia"]

EXCLUDED_PART_TERMS = [
    "rivet", "clip", "nut", "bolt", "fastener", "retainer", "screw", "washer", "grommet", "pin"
]

SUGGESTIONS = [
    "prep unprimed bumper",
    "adhesion promoter",
    "flex additive",
    "static neutralization",
    "mask for texture",
    "mask for two tone",
    "ADD for parking sensors",
    "ADD for auto park",
    "ADD if required - transfer parking sensor brackets",
    "IF LKQ ADD DETRIM TO ALL BUMPER COMPONENTS"
]

def bumper_replace_rule(lines, seen):
    print("🚀 bumper_replace_rule fired")
    section_lines = []
    triggers = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[BUMPER REPLACE RULE] Scanning line: {norm}")

        # ✅ Phrase-level detection with subcomponent filtering
        for phrase in REPLACE_PHRASES:
            if phrase in norm:
                if any(term in norm for term in EXCLUDED_PART_TERMS):
                    print(f"[BUMPER REPLACE RULE] ⛔ Skipped subcomponent line: {norm}")
                    continue
                triggers.append(f"Phrase: {phrase}")
                print(f"[BUMPER REPLACE RULE] ✅ Phrase detected: {phrase}")

        # ✅ Contextual detection for generic terms
        if any(term in norm for term in GENERIC_BUMPER_TERMS):
            if "bumper" in norm or "cover" in norm:
                if not any(term in norm for term in EXCLUDED_PART_TERMS):
                    triggers.append(f"Contextual term: {norm}")
                    print(f"[BUMPER REPLACE RULE] ✅ Contextual bumper term detected: {norm}")
                else:
                    print(f"[BUMPER REPLACE RULE] ⛔ Skipped generic subcomponent line: {norm}")

        # ✅ Mitchell-style trigger detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if "remove" in prev_norm and "bumper cover" in prev_norm:
                if "/ replace" in norm or "/ install" in norm:
                    triggers.append("Mitchell-style trigger")
                    print(f"[BUMPER REPLACE RULE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")

    if triggers:
        missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
        if missing:
            print(f"[BUMPER REPLACE RULE] 🎯 Suggestions returned: {missing}")
            print(f"[BUMPER REPLACE RULE] 🔍 Trigger sources: {triggers}")
            return ("BUMPER REPLACEMENT CHECK", missing)

    return None

def register():
    print("✅ bumper_replace_rule registered")
    return [bumper_replace_rule]
