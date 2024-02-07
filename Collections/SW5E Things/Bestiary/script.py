import json
import urllib.request

to_automate_keywords = ["saving throw", "dc", "shocked until"]
def processBestiaryBuilderAPI(bestiaryID, fileName, autoMode):
    url = f"https://bestiarybuilder.com/api/export/bestiary/{bestiaryID}"
    r = urllib.request.urlopen(url)
    data = json.load(r)

    count = 0
    saveAuto = []
    creatures = data.get('creatures', [])
    name = data.get('metadata', {}).get('name')

    source = {"name": name,
              "type": "Custom",
              "shortname": "".join([s[0] for s in data.get('metadata', {}).get('name',"").split()]),
              "link": ""}

    kfcdb = {
        "sources": [source],
        "monsters": []
    }

    for mon in creatures:
        monster = {
            "name": mon.get('name'),
            "cr": mon.get('cr'),
            "size": mon.get('size'),
            "type": mon.get('race'),
            "tags": "",
            "section": "Star Wars",
            "alignment": mon.get('alignment'),
            "environment": "Custom",
            "ac": mon.get('ac'),
            "hp": mon.get('hp'),
            "init": mon.get('ability_scores',{}).get('prof_bonus') + ((mon.get('ability_scores',{}).get('dexterity')-10)/2),
            "lair": "",
            "legendary": "",
            "unique": "",
            "sources": f"{name}: {len(kfcdb['monsters'])+1}"
        }

        kfcdb['monsters'].append(monster)
        count += 1

        actions = mon.get('actions', [])

        for a in actions:
            if a.get('description') and any(x in a.get('description').lower() for x in to_automate_keywords):
                try:
                    auto=a.get('automation',{})
                    if isinstance(auto, list):
                        auto=auto[0]
                    auto=auto.get('automation',[])
                except:
                    auto=[]
                    pass
                auto_type = []
                for obj in auto:
                    get_type(obj, auto_type)

                s = {"name": mon.get('name'), 'ability': a.get('name'),
                     'complete': True if any(x in auto_type for x in ["roll", "ieffect2", "save", "variable"]) else False,
                     'test': auto_type,
                     'auto': auto}
                saveAuto.append(s)

    with open(fileName, "w") as outfile:
        json.dump(kfcdb, outfile)

    if autoMode == "a":
        mf = open("automation.json", encoding='utf-8')
        autoMon = json.load(mf)
        autoMon = autoMon + saveAuto
    else:
        autoMon = saveAuto

    with open("automation.json", "w") as outfile:
        json.dump(autoMon, outfile)

    with open("Critter Todo.py", "w") as outfile:
        for x in autoMon:
            if x['complete'] == False:
                outfile.write(f"# TODO {x.get('name')}: {x.get('ability')}\n")

    print(f'Complete! {count} monsters processed for {name}.\nMonster actions to automate: {sum(x["complete"] == False for x in saveAuto)} out of {len(saveAuto)}\n')

def get_type(object, type_list):
    obj_type = object.get('type')

    if obj_type:
        type_list.append(obj_type)
        if obj_type == "ieffect2":
            return

    if "effects" in object.keys():
        for child in object["effects"]:
            get_type(child, type_list)
    elif "automation" in object.keys():
        for child in object["automation"]:
            get_type(child, type_list)
    elif "hit" in object.keys():
        for child in object["hit"]:
            get_type(child,type_list)

processBestiaryBuilderAPI("65a99d77e03abba02d8599c1",'KFC Ground.json', "w")
processBestiaryBuilderAPI("65a9a0e2b4f2853f0d4cbba4",'KFC Space.json', "a")