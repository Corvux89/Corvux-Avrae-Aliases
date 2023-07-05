import json

f = open('spellbook.json', encoding='utf-8')

spells = json.load(f)
out_dict = {}

out_dict["total"] = len(spells)
out_dict["Force"] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
out_dict["Tech"] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
out_dict["dex"] = 0

for sp in spells:
    try:
        out_dict[sp.get("school")][sp.get('level')] += 1
    except KeyError:
        print(f"Error with {sp}")

    if 'description' in sp and "dexterity saving" in sp.get('description').lower():
        out_dict["dex"] += 1


print(f"Total Spells: {out_dict['total']}\nForce Powers: {out_dict['Force']}\nTech Power: {out_dict['Tech']}"
      f"\nDex saves: {out_dict['dex']}")

