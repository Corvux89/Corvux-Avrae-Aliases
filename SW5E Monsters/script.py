import json
from fractions import Fraction


def processJSON(f, name, fileName, autoMode):
    count = 0
    critdb = json.load(f)
    saveAuto = []

    source = {}
    source["name"] = name
    source["type"] = "Custom"
    source["shortname"] = "".join([s[0] for s in name.split()])
    source["link"] = ""

    kfcdb = {}
    kfcdb["sources"] = []
    kfcdb["sources"].append(source)
    kfcdb["monsters"] = []

    for critter in critdb["creatures"]:
        monster = {}
        monster["name"] = critter.get("name")
        monster["cr"] = str(Fraction(critter["stats"].get("challengeRating")))
        monster["size"] = critter["stats"].get("size")
        monster["type"] = critter["stats"].get("race")
        monster["tags"] = critter["flavor"].get("faction")
        monster["section"] = "Star Wars"
        monster["alignment"] = critter["stats"].get("alignment")
        monster["environment"] = "Custom"
        monster["ac"] = critter["stats"].get("armorClass")
        monster["hp"] = critter["stats"].get("hitPoints")
        monster["init"] = critter["stats"]["abilityScoreModifiers"].get("dexterity") + critter["stats"].get(
            "proficiencyBonus")
        monster["lair"] = ""
        monster["legendary"] = ""
        monster["unique"] = ""
        monster["sources"] = f"{name}: {len(kfcdb['monsters']) + 1}"

        kfcdb["monsters"].append(monster)
        count += 1

        actions = critter["stats"].get("actions")

        for a in actions:
            if "saving throw" in a.get("description").lower() and "<avrae hidden>" not in a.get("description").lower():
                s = {"name": critter.get('name'), 'ability': a.get('name')}
                saveAuto.append(s)

    with open(fileName, "w") as outfile:
        json.dump(kfcdb, outfile)

    with open("automation.json", autoMode) as outfile:
        json.dump(saveAuto, outfile)

    print(f'Complete! {count} monsters processed for {name}.\nMonster actions to automate: {len(saveAuto)}\n')



f = open('CritterDB - Ground.json', encoding='utf-8')
processJSON(f, "Resolute - Ground", "KFC Ground.json", "w")

f = open('Critter DB - Space.json', encoding='utf-8')
processJSON(f, "Resolute - Space", "KFC Space.json", "a")