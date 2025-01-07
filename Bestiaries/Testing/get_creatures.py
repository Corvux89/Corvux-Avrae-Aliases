import json
import urllib.request

def getBB(bestiaryID, fileName):
    url = f"https://bestiarybuilder.com/api/export/bestiary/{bestiaryID}"
    r = urllib.request.urlopen(url)
    data = json.load(r)

    with open(fileName, "w") as outfile:
        outfile.write(json.dumps(data['creatures'], indent=2))


getBB('65a9a408696ceb447200763d', 'Bestiaries\\Testing\\test.json')


