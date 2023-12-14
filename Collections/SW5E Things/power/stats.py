import json

f = open('spellbook.json', encoding='utf-8')

spells = json.load(f)
out_dict = {}

out_dict["total"] = len(spells)
out_dict["Force"] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
out_dict["Tech"] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
out_dict["automated"] = 0
out_dict["todo"] = []

for sp in spells:
    try:
        out_dict[sp.get("school")][sp.get('level')] += 1
    except KeyError:
        print(f"Error with {sp}")

    if sp.get("automation") and len(sp["automation"]) >=1:
        out_dict["automated"] += 1
    else:
        out_dict["todo"].append(sp.get('name'))


print(f"Total Spells: {out_dict['total']} ({out_dict['automated']} automated)\nForce Powers: {out_dict['Force']}\nTech Power: {out_dict['Tech']}")


with open("Powers Todo.py", "w") as outfile:
    for x in out_dict["todo"]:
        outfile.write(f"# TODO: {x}\n")
