import json

f = open('scratch.json', encoding='utf-8')
stuff = json.load(f)
todos = []

for thing in stuff:
    new_thing = {"name": thing.get('name')}
    if thing.get('level'):
        new_thing["level"] = thing.get('level')

    if thing.get('action'):
        new_thing["actions"] = [{"action": thing.get('action')}]

    if thing.get('counter'):
        new_thing["counters"] = [thing.get('counter')]

    if thing.get('modCounter'):
        new_thing["modCounter"] = thing.get('modCounter')

    if thing.get('modCVAR'):
        new_thing["modCVAR"] = thing.get('modCVAR')

    todos.append(new_thing)


with open('out.json', 'w') as outfile:
    json.dump(todos, outfile)

