import json

total_count = 0

f=open('weapons A.json', encoding='utf-8')
total_count += len(json.load(f))

f = open('weapons C.json', encoding='utf-8')
total_count += len(json.load(f))

f = open('weapons D-G.json', encoding='utf-8')
total_count += len(json.load(f))

f = open('weapons H-R.json', encoding='utf-8')
total_count += len(json.load(f))

f = open('weapons R-S.json', encoding='utf-8')
total_count += len(json.load(f))

f = open('weapons T-Z.json', encoding='utf-8')
total_count += len(json.load(f))

print(total_count)
