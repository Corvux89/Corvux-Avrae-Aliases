import json
import os

total_count = 0

for filename in os.listdir('json'):
    f = open(os.path.join('json', filename), encoding='utf-8')
    actions = json.load(f)
    total_count += len(actions)

print(f"Total Actions supported: {total_count}")
