import json
import urllib.request as rq

url = "https://sw5eapi.azurewebsites.net/api/power"
spell_map = {}

with open('Homebrew\Resolute Spellbook\\60f243f60dc83c7c1d3a37cc.spell', encoding='utf-8', mode='r') as outfile:
    spells = json.load(outfile)

with open('Collections\SW5E Things\power gvars\Force Powers - b3458e30-e3ca-4674-970c-adc8987e5b07.json', encoding='utf-8', mode='r') as outfile:
    spell_map = json.load(outfile)

with open('Collections\SW5E Things\power gvars\Tech Powers - e90cc412-c2ad-4c2f-8e48-8ccc81fb5bf9.json', encoding='utf-8', mode='r') as outfile:
    spell_map.update(json.load(outfile))

spell_map = list(spell_map.keys())

r = rq.urlopen(url)

# Get this script out of my todolist
key = "TODO"

site_spells = json.load(r)
site_list = [x.get('name') for x in site_spells]

# Expanded Tech Powers
# https://www.gmbinder.com/share/-MDp2nOeGD6JJLxNM_lT
# Expanded Force Powers
# https://www.gmbinder.com/share/-MDosNzOCLn0_ColYfBf
# New Tech Powers Aziz
# https://www.gmbinder.com/share/-My-EnFn7t2vE3kxawC0

with open("Homebrew\expanded.json", "r") as outfile:
    expanded_list = json.load(outfile)

with open('Homebrew\\aziz.json', "r") as outfile:
    aziz_list = json.load(outfile)

out_dict = {}
mapping_list = []

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

        auto = json.dumps(sp["automation"])

    else:
        out_dict["todo"].append(sp.get('name'))

    formatted_name = sp.get('name').replace('(SW) ', '')

    if formatted_name in site_list:
        found = True
        site_list.remove(formatted_name)

    if formatted_name in expanded_list:
        found = True
        expanded_list.remove(formatted_name)

    if formatted_name in aziz_list:
        found = True
        aziz_list.remove(formatted_name)

    if found and sp.get('name').lower() not in spell_map and formatted_name.lower() not in spell_map:
        mapping_list.append(sp.get('name'))



print(f"Total Spells: {out_dict['total']} ({out_dict['automated']} automated)\n"
      f"Force Powers: {out_dict['Force']}\n"
      f"Tech Power: {out_dict['Tech']}\n"
      f"Missing Powers: {len(site_list)+len(expanded_list)+len(aziz_list)}\n"
      f"Missing Mappings: {len(mapping_list)}\n"
      f"Total TODO: {len(site_list)+len(expanded_list)+len(aziz_list)+len(out_dict['todo'])+len(mapping_list)}")


with open("Homebrew\\Resolute Spellbook\\Powers Todo.py", "w") as outfile:
    for x in mapping_list:
        outfile.write(f'# {key}: Mapping Missing {x}\n')

    for x in site_list:
        outfile.write(f"# {key}: Source Missing {x}\n")

    for x in expanded_list:
        outfile.write(f"# {key}: Expanded Missing {x}\n")
    
    for x in aziz_list:
        outfile.write(f"# {key}: Aziz Tech Power Missing {x}\n")

    for x in out_dict["todo"]:
        outfile.write(f"# {key}: {x}\n")
