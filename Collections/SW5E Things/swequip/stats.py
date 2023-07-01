import json
import os

total_count = 0

for filename in os.listdir('weapons'):
    f=open(os.path.join('weapons', filename), encoding='utf-8')
    total_count += len(json.load(f))

print(f"Total Weapons: {total_count}")
