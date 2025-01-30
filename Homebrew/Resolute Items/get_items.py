import os
import json
import urllib.request as rq

header = {"Authorization": os.environ.get('AVRAE_TOKEN')}

# Resolute Items
# https://www.gmbinder.com/share/-ODwGI3WLonaqXgRUZW8

# Drake's new items
# https://www.gmbinder.com/share/-LrbH9XK6HZH_jLVI3sX

req = rq.Request('https://api.avrae.io/homebrew/items/65e040c041dbbf86ba9a4631', headers=header)

request = rq.urlopen(req)
item_data = json.load(request)

items = item_data['data']['items']

out_dict = {}

out_dict["total"] = len(items)


print(f"Total Items: {out_dict['total']}\n")


with open('Homebrew\\Resolute Items\\items.json', encoding='utf-8', mode="w+") as outfile:
    outfile.write(json.dumps(sorted(items, key=lambda item: item['name'].replace('(SW) ', '')), indent=2))
