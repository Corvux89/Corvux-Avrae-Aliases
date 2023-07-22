import json
from fractions import Fraction


def processJSON(f, name, fileName):
    count = 0
    critdb = json.load(f)
    saveAuto = []

    source = {}
    source["name"] = name
    source["type"] = "Custom"
    source["shortname"] = "CS"
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
        monster["sources"] = f"Resolute: {len(kfcdb['monsters']) + 1}"

        kfcdb["monsters"].append(monster)
        count += 1

        actions = critter["stats"].get("actions")

        for a in actions:
            if "saving throw" in a.get("description").lower():
                saveAuto.append(f"{critter.get('name')}|{a.get('name')}")

    with open(fileName, "w") as outfile:
        json.dump(kfcdb, outfile)

    s_str = "\n".join(x for x in saveAuto)
    with open("automation.txt", "w") as outfile:
        outfile.write(s_str)

    s_str = "\n".join(x for x in saveAuto)
    print(f'Complete! {count} monsters processed.\nMonster actions to automate: {len(saveAuto)}')



f = open('CritterDB - Ground.json', encoding='utf-8')
processJSON(f, "Resolute - Ground", "KFC Ground.json")

f = open('Critter DB - Space.json', encoding='utf-8')
processJSON(f, "Resolute - Space", "KFC Space.json")