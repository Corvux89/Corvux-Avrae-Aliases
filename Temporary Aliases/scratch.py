import json

f = open('scratch.json', encoding='utf-8')
stuff = json.load(f)
todos = []

f = open('out.json', encoding='utf-8')
already_done = json.load(f)

maneuvers = {x["name"] for x in already_done}

for thing in stuff:
    if thing["name"] not in maneuvers:
        todos.append(thing["name"])

with open('out.json', 'w') as outfile:
    json.dump(todos, outfile)

