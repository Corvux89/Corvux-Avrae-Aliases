import json, os, requests
import urllib.request as rq

url = 'https://api.avrae.io/homebrew/spells/60f243f60dc83c7c1d3a37cc'
header = {"Authorization": os.environ.get('AVRAE_TOKEN')}

with open('Homebrew\Resolute Spellbook\spellbook.json', encoding='utf-8', mode='r') as outfile:
    data = json.load(outfile)

request = requests.get(url, headers=header)

tome = json.loads(request.text)['data']

tome['spells'] = data

out = requests.put(url, json=tome, headers=header)
