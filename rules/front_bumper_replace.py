import re
from utils import normalize, normalize_orientation, normalize_operation, suggest_if_missing

REPLACE_PHRASES = [
    "repl bumper", "replace bumper",
    "repl bumper cover", "replace bumper cover",
    "repl fascia", "replace fascia",
    "repl bumper cover assy", "replace bumper cover assy",
    "repl bumper cover assembly", "replace bumper cover assembly",
    "upper cover", "fascia"
]

SUGGESTIONS = [
    "flex additive",
    "adhesion promoter",
    "static neutralization",
    "mask for texture",
    "mask for two tone",
    "ADD for parking sensors",
    "ADD for auto park",
    "ADD if required - transfer parking sensor brackets",
    "IF LKQ ADD DETRIM TO ALL BUMPER COMPONENTS"
]

def front_bumper_replace_rule(lines, seen):
    print("🚀 front_bumper_replace_rule fired")
    bumper_context_detected = False
    phrase_detected = False
    mitchell_triggered = False
    section_lines = []

    for i in range(len(lines)):
        norm = normalize_operation(normalize_orientation(lines[i]))
        section_lines.append(lines[i])
        print(f"[FRONT BUMPER REPLACE RULE] Scanning line: {norm}")

        # ✅ Context detection
        if "front bumper" in norm or "bumper cover" in norm or "fascia" in norm:
            bumper_context_detected = True
            print("[FRONT BUMPER REPLACE RULE] ✅ Context match")

        # ✅ Phrase-level detection
        for phrase in REPLACE_PHRASES:
            if phrase in norm:
                phrase_detected = True
                print(f"[FRONT BUMPER REPLACE RULE] ✅ Phrase detected: {phrase}")

        # ✅ Mitchell-style trigger detection
        if i > 0:
            prev_norm = normalize_operation(normalize_orientation(lines[i - 1]))
            if ("remove" in prev_norm and "bumper cover" in prev_norm) and ("/ replace" in norm or "/ install" in norm):
                mitchell_triggered = True
                print(f"[FRONT BUMPER REPLACE RULE] ✅ Mitchell-style trigger matched at index {i-1}/{i}")

    if (bumper_context_detected and phrase_detected) or mitchell_triggered:
        missing = suggest_if_missing(section_lines, SUGGESTIONS, seen)
        if missing:
            print(f"[FRONT BUMPER REPLACE RULE] 🎯 Suggestions returned: {missing}")
            return ("FRONT BUMPER REPLACEMENT CHECK", missing)

    return None

def register():
    print("✅ front_bumper_replace_rule registered")
    return [front_bumper_replace_rule]