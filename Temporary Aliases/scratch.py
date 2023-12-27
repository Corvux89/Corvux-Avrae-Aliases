import json

f = open('scratch.json', encoding='utf-8')
stuff = json.load(f)
todos = []

for thing in stuff:
    print(f'# TODO: {thing["name"]}')
