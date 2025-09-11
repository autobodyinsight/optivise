import re
from utils import normalize

def build_origin_check_rule(lines, seen):
    print("🚀 build_origin_check_rule fired")

    vin = None
    origin = None

    # 🔍 Extract VIN
    for line in lines:
        norm = normalize(line)
        vin_match = re.search(r"\bvin[:\s]*([a-hj-npr-z0-9]{17})\b", norm)
        if vin_match:
            vin = vin_match.group(1).upper()
            break
        standalone_match = re.search(r"\b[a-hj-npr-z0-9]{17}\b", norm)
        if standalone_match:
            vin = standalone_match.group(0).upper()
            break

    if not vin:
        print("[BUILD ORIGIN CHECK] ❌ No VIN found, skipping rule")
        return None

    # 🌍 Determine build origin
    prefix = vin[:2]
    first = vin[0]

    if prefix in ["RF", "RK"]:
        origin = "Taiwan"
    elif prefix in ["3A", "3W"]:
        origin = "Mexico"
    elif first == "J":
        origin = "Japan"
    elif first == "K":
        origin = "Korea"
    elif first == "L":
        origin = "China"
    elif first in ["1", "4", "5"]:
        origin = "United States"
    elif first == "2":
        origin = "Canada"

    if not origin:
        print("[BUILD ORIGIN CHECK] ❌ No origin derived from VIN")
        return None

    print(f"[BUILD ORIGIN CHECK] ✅ VIN: {vin} → Origin: {origin}")

    # 🔍 Scan for mismatched build origin mentions
    mismatches = []
    origin_lower = origin.lower()
    found = False

    for line in lines:
        norm = normalize(line).lower()
        match = re.search(r"\b(japan|korea|china|taiwan|united states|canada|mexico)\b.*\b(build|built)\b", norm)
        if match:
            found = True
            mentioned = match.group(1)
            if mentioned != origin_lower:
                mismatches.append(
                    f"⚠️ Build origin mismatch: '{line.strip()}' mentions '{mentioned.title()}' but VIN indicates '{origin}'"
                )

    if not found:
        print("[BUILD ORIGIN CHECK] ℹ️ No build origin mentioned in estimate, skipping suggestions")
        return None

    if mismatches:
        print(f"[BUILD ORIGIN CHECK] 🎯 Mismatches found: {len(mismatches)}")
        return ("VERIFY VEHICLE BUILD ORIGIN", mismatches)

    return None

def register():
    print("✅ build_origin_check_rule registered")
    return [build_origin_check_rule]