import pandas as pd
import requests

league = "Sanctum"
alt_qualities = ["Divergent", "Anomalous", "Phantasmal"]

response = requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=SkillGem").json()


def is_alt_quality(gem):
    for alt_quality in alt_qualities:
        if alt_quality in gem["name"]:
            return True


def is_corrupted(gem):
    if "corrupted" not in gem.keys():
        return False
    return gem["corrupted"]


def get_level(gem):
    if "gemLevel" not in gem.keys():
        return -1
    return gem["gemLevel"]


def get_quality(gem):
    if "gemQuality" not in gem.keys():
        return -1
    return gem["gemQuality"]


def is_max_level(gem):
    if "gemLevel" not in gem.keys():
        return False
    return gem["gemLevel"] >= 20


# Get gem values
alt_quality_gems = []
for gem in response["lines"]:
    if is_alt_quality(gem) and not is_max_level(gem) and not is_corrupted(gem):
        alt_quality_gems.append({"name": gem["name"].lower().replace("'", ""), "gem_level": get_level(gem), "gem_quality": get_quality(gem), "chaos_value": gem["chaosValue"],
                                 "divine_value": gem["divineValue"]})
alt_quality_gems = sorted(alt_quality_gems, key=lambda x: x["name"])

# Get highest value version
filtered_gems = []
highest_value_version = alt_quality_gems[0]
for gem in alt_quality_gems:
    if gem["name"] != highest_value_version["name"]:
        filtered_gems.append(highest_value_version)
        highest_value_version = gem

    if gem["chaos_value"] > highest_value_version["chaos_value"]:
        highest_value_version = gem

data = pd.DataFrame(filtered_gems)
data.to_csv("./prices.csv", index=False)
