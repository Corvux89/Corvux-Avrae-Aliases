import json

f = open('scratch.json', encoding='utf-8')

objects = json.load(f)
todo = []


for o in objects:
 todo.append(o.get("name"))

with open("../Collections/SW5E Things/swsetup/feats todo.py", "w") as outfile:
 for x in todo:
  outfile.write(f"# TODO: {x}\n")
