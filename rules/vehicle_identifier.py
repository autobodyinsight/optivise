import re
from utils import normalize

def vehicle_identifier_rule(lines, seen):
    print("🚀 vehicle_identifier_rule fired")

    vehicle_info = None
    vin = None
    origin = None

    # 🔍 Extract vehicle description and VIN
    for line in lines:
        norm = normalize(line)

        # Match CCC or Mitchell-style vehicle description
        if not vehicle_info and re.search(r"\b\d{4}\b.*\bkia\b.*\bniro\b", norm):
            vehicle_info = line.strip()
            print(f"[VEHICLE IDENTIFIER] ✅ Vehicle info found: {vehicle_info}")

        # Match VIN (prefixed or standalone)
        if not vin:
            vin_match = re.search(r"\bvin[:\s]*([a-hj-npr-z0-9]{17})\b", norm)
            if vin_match:
                vin = vin_match.group(1).upper()
                print(f"[VEHICLE IDENTIFIER] ✅ VIN found (prefixed): {vin}")
            else:
                standalone_match = re.search(r"\b[a-hj-npr-z0-9]{17}\b", norm)
                if standalone_match:
                    vin = standalone_match.group(0).upper()
                    print(f"[VEHICLE IDENTIFIER] ✅ VIN found (standalone): {vin}")

    # 🌍 Determine build origin from VIN
    if vin and len(vin) == 17:
        prefix = vin[:2]
        first = vin[0]

        origin_map = {
            "RF": "Taiwan", "RK": "Taiwan",
            "3A": "Mexico", "3W": "Mexico",
            "J": "Japan", "K": "Korea", "L": "China",
            "1": "United States", "4": "United States", "5": "United States",
            "2": "Canada"
        }

        origin = origin_map.get(prefix) or origin_map.get(first)
        if origin:
            print(f"[VEHICLE IDENTIFIER] 🌍 Built Origin: {origin}")

    # 📦 Final output
    if vehicle_info or vin:
        output = []
        if vehicle_info:
            output.append(f"📌 Vehicle: {vehicle_info}")
        if vin:
            output.append(f"🔑 VIN: {vin}")
        if origin:
            output.append(f"🌍 Built Origin: {origin}")
        print("\n".join(output))
        return ("VEHICLE IDENTIFIER", output)

    return None

def register():
    print("✅ vehicle_identifier_rule registered")
    return [vehicle_identifier_rule]