import os, json, requests

header = {"userToken": os.environ.get('BB_TOKEN')}

def updateBestiary(bestiaryID, sourceFile):
    with open(sourceFile, encoding='utf-8', mode='r') as outfile:
        data = json.load(outfile)

    request = requests.get(f"https://bestiarybuilder.com/api/export/bestiary/{bestiaryID}")

    bestiary = json.loads(request.text)['metadata']

    bestiary['creatures'] = data

    session = requests.Session()
    session.cookies.update(header)


    out = session.post(f"https://bestiarybuilder.com/api/bestiary/{bestiaryID}/update", headers=header, data=json.dumps({"data": bestiary}))

    if out.status_code != 200:
        print(out.text)
    else:
        print("Complete!")



updateBestiary('65a9a408696ceb447200763d', 'Bestiaries\\Testing\\test.json')