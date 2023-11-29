import json

f = open('equipment.json', encoding='utf-8')
equipment = json.load(f)
weapons = []
ammo = []

for equip in equipment:
    if equip.get("equipmentCategory") == "Weapon":
        weapons.append({"name": equip.get("name"),
                        "damageNumberOfDice": equip.get("damageNumberOfDice"),
                        "damageType": equip.get("damageType"),
                        "weaponClassification": equip.get("weaponClassification"),
                        "damageDieType": equip.get("damageDieType"),
                        "properties": equip.get("properties"),
                        "propertiesMap": equip.get("propertiesMap")
                        })
    elif equip.get("equipmentCategory") == "Ammunition":
        ammo.append()

with open('weapons.json', 'w') as outfile:
    json.dump(weapons, outfile)

