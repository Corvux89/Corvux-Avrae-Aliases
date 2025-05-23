import json
import urllib.request
import re

print("Starting")

to_automate_keywords = ["saving throw", "dc", "shocked until", 'to hit']
to_automate_exclude_names = ['forcecasting', 'tech-casting', 'techcasting', 'innate tech casting']

automation_file = "Bestiaries\\Resolute Bestiary\\automation.json"
todo_file = "Bestiaries\\Resolute Bestiary\\Critter Todo.py"


def processBeastiaryBuilderAPI(BeastiaryID, fileName, autoMode, creatureFile):
    url = f"https://bestiarybuilder.com/api/export/bestiary/{BeastiaryID}"
    r = urllib.request.urlopen(url)
    data = json.load(r)

    print(f"Data Loaded from {url}")

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
            "init": round(mon.get('ability_scores',{}).get('prof_bonus') + ((mon.get('ability_scores',{}).get('dexterity')-10)/2)),
            "lair": "",
            "legendary": "",
            "unique": "",
            "sources": f"{name}: {len(kfcdb['monsters'])+1}"
        }

        kfcdb['monsters'].append(monster)
        count += 1

        actions = (mon.get('actions', []) + 
                   mon.get('traits', []) + 
                   mon.get('bonus_actions', []) + 
                   mon.get('reactions', []) + 
                   mon.get('legactions', []) + 
                   mon.get('mythic', []) + 
                   mon.get('lair', []) + 
                   mon.get('regional', [])
                   )

        for a in actions:
            if ((a.get('description') and any(
                re.search(rf'\b{x}\b', a.get('description').lower())
                for x in to_automate_keywords
            )) or (a.get('name') and 'recharge' in a.get('name').lower()
                   )) and (a.get('name') and a.get('name').lower() not in to_automate_exclude_names):
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
                     'complete': True if any(x in auto_type for x in ["roll", "ieffect2", "save", "variable", "check", "temphp", "condition", 'attack']) else False,
                     'source': name}

                if not s['complete']:
                    s['description'] = a.get('description')
                    s['automation'] = a.get('automation', {})
                saveAuto.append(s)
    if fileName:
        with open(fileName, "w") as outfile:
            json.dump(kfcdb, outfile)

    if creatureFile:
        with open(creatureFile, "w") as outfile:
            outfile.write(json.dumps(creatures, indent=2))

    if autoMode == "a":
        mf = open(automation_file, encoding='utf-8')
        autoMon = json.load(mf)
        autoMon = autoMon + saveAuto
    else:
        autoMon = saveAuto

    with open(automation_file, "w") as outfile:
        json.dump(autoMon, outfile, indent=2)

    with open(todo_file, "w") as outfile:
        for x in autoMon:
            if x['complete'] == False:
                outfile.write(f"# TODO [{x.get('source')}]: {x.get('name')} ({x.get('ability')})\n")

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

processBeastiaryBuilderAPI("67606b7cd4d3ec37d67ec64a", 'Bestiaries\\Resolute Bestiary\\KFC Ground.json', "w", 'Bestiaries\\Resolute Bestiary\\Resolute Ground.json')