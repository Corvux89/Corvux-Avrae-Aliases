import json, os, requests

url = 'https://api.avrae.io/homebrew/items/65e040c041dbbf86ba9a4631'
header = {"Authorization": os.environ.get('AVRAE_TOKEN')}

with open('Homebrew\Resolute Items\items.json', encoding='utf-8', mode='r') as outfile:
    data = json.load(outfile)

request = requests.get(url, headers=header)

tome = json.loads(request.text)['data']

tome['items'] = data

out = requests.put(url, json=tome, headers=header)

if out.status_code != 200:
    print(out.text)
else:
    print("Complete!")