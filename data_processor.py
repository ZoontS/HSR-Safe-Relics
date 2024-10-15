import json

available_stats = {
    "Body": {"HP%": 0, "ATK%": 0, "DEF%": 0, "CRIT Rate": 0, "CRIT DMG": 0, "Outgoing Healing": 0, "Effect HIT Rate": 0},
    "Feet": {"HP%": 0, "ATK%": 0, "DEF%": 0, "Speed": 0},
    "Planar Sphere": {"HP%": 0, "ATK%": 0, "DEF%": 0, "Physical DMG": 0, "Fire DMG": 0, "Ice DMG": 0, "Lightning DMG": 0, "Wind DMG": 0, "Quantum DMG": 0, "Imaginary DMG": 0},
    "Link Rope": {"Break Effect": 0, "Energy Regen Rate": 0, "HP%": 0, "ATK%": 0, "DEF%": 0}
}

with open("Relic Data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
available_relics = data["Available Relics"]["Relics"]
available_ornaments = data["Available Relics"]["Planar Ornaments"]
available_relics_stats = {}
available_ornaments_stats = {}

for relic in available_relics:
    available_relics_stats[relic] = {"Body": available_stats["Body"].copy(), "Feet": available_stats["Feet"].copy()}
for ornament in available_ornaments:
    available_ornaments_stats[ornament] = {"Planar Sphere": available_stats["Planar Sphere"].copy(), "Link Rope": available_stats["Link Rope"].copy()}

for character in data["Relic Stats"]:
    for relic in data["Relic Stats"][character]["Relics"]:
        for stat in data["Relic Stats"][character]["Stats"]["Body"]:
                if stat == "Anything":
                      for i in available_relics_stats[relic]["Body"]:
                            available_relics_stats[relic]["Body"][i] += 1
                else:
                    available_relics_stats[relic]["Body"][stat] += 1
        for stat in data["Relic Stats"][character]["Stats"]["Feet"]:
                if stat == "Anything":
                      for i in available_relics_stats[relic]["Body"]:
                            available_relics_stats[relic]["Body"][i] += 1
                else:
                    available_relics_stats[relic]["Feet"][stat] += 1
    for ornament in data["Relic Stats"][character]["Planar Ornaments"]:
        for stat in data["Relic Stats"][character]["Stats"]["Planar Sphere"]:
                if stat == "Anything":
                      for i in available_relics_stats[relic]["Body"]:
                            available_relics_stats[relic]["Body"][i] += 1
                else:
                    available_ornaments_stats[ornament]["Planar Sphere"][stat] += 1
        for stat in data["Relic Stats"][character]["Stats"]["Link Rope"]:
                if stat == "Anything":
                      for i in available_relics_stats[relic]["Body"]:
                            available_relics_stats[relic]["Body"][i] += 1
                else:
                    available_ornaments_stats[ornament]["Link Rope"][stat] += 1

# print(f"Relics: {available_relics_stats}")
# print()
# print(f"Planar Ornaments: {available_ornaments_stats}")

relic_occurence = {}
ornament_occurence = {}

for relic, pieces in available_relics_stats.items():
    for piece, stats in pieces.items():
        for stat, num in stats.items():
            if num not in relic_occurence:
                relic_occurence[num] = {relic: {piece: [stat]}}
                continue
            if relic not in relic_occurence[num]:
                relic_occurence[num][relic] = {piece: [stat]}
                continue
            if piece not in relic_occurence[num][relic]:
                relic_occurence[num][relic][piece] = [stat]
                continue
            relic_occurence[num][relic][piece].append(stat)
for relic, pieces in available_ornaments_stats.items():
    for piece, stats in pieces.items():
        for stat, num in stats.items():
            if num not in ornament_occurence:
                ornament_occurence[num] = {relic: {piece: [stat]}}
                continue
            if relic not in ornament_occurence[num]:
                ornament_occurence[num][relic] = {piece: [stat]}
                continue
            if piece not in ornament_occurence[num][relic]:
                ornament_occurence[num][relic][piece] = [stat]
                continue
            ornament_occurence[num][relic][piece].append(stat)

relic_occurence = dict(sorted(relic_occurence.items()))
ornament_occurence = dict(sorted(ornament_occurence.items()))

combined_occurence = {"Relics": relic_occurence, "Planar Ornaments": ornament_occurence}

with open("Relic Occurences.json", "w", encoding="utf-8") as f: 
    print(json.dumps(combined_occurence, ensure_ascii=False, indent=4), file=f)