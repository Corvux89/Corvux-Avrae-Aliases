import json
import urllib.request

import requests

url = "https://sw5eapi.azurewebsites.net/api/power"
request = requests.get('https://api.avrae.io/homebrew/spells/60f243f60dc83c7c1d3a37cc')
spells = json.loads(request.text)['data']['spells']

r = urllib.request.urlopen(url)

site_spells = json.load(r)
site_list = [x.get('name') for x in site_spells]

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

    formatted_name = sp.get('name').replace('(SW) ', '')

    if formatted_name in site_list:
        site_list.remove(formatted_name)


print(f"Total Spells: {out_dict['total']} ({out_dict['automated']} automated)\n"
      f"Force Powers: {out_dict['Force']}\n"
      f"Tech Power: {out_dict['Tech']}\n"
      f"Missing Powers: {len(site_list)}")


with open("Powers Todo.py", "w") as outfile:
    for x in site_list:
        outfile.write(f"# TODO: Missing {x}\n")

    for x in out_dict["todo"]:
        outfile.write(f"# TODO: {x}\n")

with open('spellbook.json', encoding='utf-8', mode="w+") as outfile:
    outfile.write(json.dumps(sorted(spells, key=lambda spell: spell['name'].replace('(SW) ', '')), indent=2))
