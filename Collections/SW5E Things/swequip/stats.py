import json
import os

total_count = 0
w_list = []

for filename in os.listdir('weapons'):
    f=open(os.path.join('weapons', filename), encoding='utf-8')
    weapons = json.load(f)
    total_count += len(weapons)
    w_list+=[w.get('name') for w in weapons]


with open("all weapons.json", "w") as outfile:
    json.dump(w_list, outfile)


print(f"Total Weapons: {total_count}")
