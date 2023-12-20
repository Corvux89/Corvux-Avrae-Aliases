import json

f = open('test.json', encoding='utf-8')
items = json.load(f)

for item in items:
    print(f"{item.get('name')}")