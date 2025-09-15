import re
from utils import normalize

def vehicle_identifier_rule(lines, seen):
    print("🚀 vehicle_identifier_rule fired")

    vin = None
    origin = None
    vehicle_info = None
    flagged_blocks = []
    used_indices = set()

    # 🔍 Extract VIN (prefixed or standalone)
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

    if not vin or len(vin) != 17:
        print("[VEHICLE IDENTIFIER] ❌ Invalid or missing VIN")
        return None

    # 🌍 Determine build origin from VIN
    prefix = vin[:2]
    first = vin[0]

    origin_map = {
        "RF": "Taiwan", "RK": "Taiwan",
        "3": "Mexico",
        "W": "Germany",
        "Y": "Sweden/Finland",
        "S": "England",
        "J": "Japan", "K": "Korea", "L": "China",
        "1": "United States", "4": "United States", "5": "United States",
        "2": "Canada"
    }

    origin = origin_map.get(prefix) or origin_map.get(first)
    if not origin:
        print("[VEHICLE IDENTIFIER] ❌ No origin derived from VIN")
        return None

    print(f"[VEHICLE IDENTIFIER] ✅ VIN: {vin} → Origin: {origin}")

    # 🚗 Identify full vehicle info line by year + vehicle keywords
    vehicle_keywords = [
        "kia", "honda", "ford", "chevy", "toyota", "bmw", "mercedes", "hyundai", "nissan",
        "utv", "sedan", "coupe", "suv", "truck", "van", "wagon", "awd", "fwd", "rwd",
        "hybrid", "gasoline", "electric", "touring", "limited", "se", "le", "xl", "xle"
    ]

    for line in lines:
        norm = normalize(line).lower()
        year_match = re.search(r"\b(19[6-9]\d|20[0-2]\d|2026)\b", norm)
        if year_match and any(keyword in norm for keyword in vehicle_keywords):
            vehicle_info = f"🚗 Vehicle Info: {line.strip()}"
            print(f"[VEHICLE IDENTIFIER] ✅ Vehicle Info: {vehicle_info}")
            break

    # 🔍 Scan for build origin mentions across lines
    origin_phrases = {
        "taiwan built": "Taiwan",
        "mexico built": "Mexico",
        "japan built": "Japan",
        "korean built": "Korea",
        "china built": "China",
        "united states built": "United States",
        "us built": "United States",
        "canada built": "Canada"
    }

    for idx in range(len(lines)):
        if idx in used_indices:
            continue

        current = normalize(lines[idx]).lower().replace("-", " ").replace(":", " ")
        next_line = normalize(lines[idx + 1]).lower().replace("-", " ").replace(":", " ") if idx + 1 < len(lines) else ""

        for phrase, expected_origin in origin_phrases.items():
            if phrase in current or phrase in next_line:
                if expected_origin != origin:
                    block = lines[idx]
                    used_indices.add(idx)

                    if phrase in next_line and idx + 1 < len(lines):
                        block += "\n" + lines[idx + 1]
                        used_indices.add(idx + 1)

                    flagged_blocks.append(
                        f"⚠️ VIN indicates '{origin}', but estimate mentions '{expected_origin}':\n{block}"
                    )
                break

    suggestions = [f"🔑 VIN: {vin}", f"🌍 Build Origin: {origin}"]
    if vehicle_info:
        suggestions.append(vehicle_info)
    if flagged_blocks:
        suggestions.extend(flagged_blocks)

    return ("VEHICLE IDENTIFIER", suggestions)
