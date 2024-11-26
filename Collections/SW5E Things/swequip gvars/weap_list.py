import json
import os
def processName(name):
    # What is the base weapon?
    out = name
    out = out.replace("Rapid - ", '').replace("Burst - ", '').replace("Two-Handed ", '').replace(" - Rifle",
                                                                                                 '').replace(" - Staff",
                                                                                                             '').replace(
        "Penetrating - ", '').replace("Corruption - ", "")
    out = out.replace("Acid - ", '').replace("Cold - ", '').replace("Fire - ", '').replace("Lightning - ", '')
    out = out.replace("Acid, ", '').replace("Cold, ", '').replace("Fire, ", '').replace("Lightning, ", '')
    out = out.replace("Rocket, Fragmentation - ", '').replace("Rocket, Incendiary - ", '').replace("Rocket, Ion - ", '')
    out = out.replace("Missile, Fragmentation - ", '').replace("Missile, Incendiary - ", '').replace("Missile, Ion - ",
                                                                                                     '')
    out = out.replace("Projector Canister, Corrosive - ", '').replace("Projector Canister, Cryo - ", '').replace(
        "Projector Canister, Incendiary - ", '')
    out = out.replace("Grapple - ", "")

    out = out.replace("Cooldown - ", "").replace("Reload - ", "")
    out = out.replace("Nano - ", "").replace("Ion Pulse - ", "").replace("Homing - ", "")

    out = stripAmmo(out)

    return out

def baseName(name):
    # What weapon is considered to be the default?
    out = name
    out = out.replace("Rapid - ", '').replace("Burst - ", '').replace("Two-Handed ", '').replace(" - Rifle",
                                                                                                 '').replace(" - Staff",
                                                                                                             '').replace(
        "Penetrating - ", '').replace("Corruption - ", "")
    out = out.replace("Cartridge, Slug - ", "")
    out = out.replace("Arrow - ", "")
    out = out.replace("Dart - ", "")
    out = out.replace("Snare - ", "")
    out = out.replace("Bolt - ", "")
    out = out.replace("Cell, Power - ", "")
    out = out.replace("Acid - ", '').replace("Cold - ", '').replace("Fire - ", '').replace("Lightning - ", '')
    out = out.replace("Acid, ", '').replace("Cold, ", '').replace("Fire, ", '').replace("Lightning, ", '')
    out = out.replace("Rocket, Fragmentation - ", '').replace("Rocket, Incendiary - ", '').replace("Rocket, Ion - ", '')
    out = out.replace("Missile, Fragmentation - ", '').replace("Missile, Incendiary - ", '').replace("Missile, Ion - ",
                                                                                                     '')
    # out = out.replace("Projector Canister, Corrosive - ", '').replace("Projector Canister, Cryo - ", '').replace(
    #     "Projector Canister, Incendiary - ", '')
    out = out.replace("Projector Tank, Corrosive - ", "").replace("Projector Tank, Cryo - ", "").replace("Projector Tank, Incendiary - ", "")
    out = out.replace("Grapple - ", "")

    out = out.replace("Cooldown - ", "").replace("Reload - ", "")
    out = out.replace("Nano - ", "").replace("Ion Pulse - ", "").replace("Homing - ", "")

    return out

def stripAmmo(name):
    out = name
    out = out.replace("Cartridge, Slug - ", '').replace("Cartridge, Corrosive - ", '').replace(
        "Cartridge, Electrifying - ", '').replace("Cartridge, Gas - ", '')
    out = out.replace("Arrow - ", '').replace("Arrow, Combustive - ", '').replace("Arrow, Electroshock - ", '').replace(
        "Arrow, Noisemaker - ", '')
    out = out.replace("Dart - ", '').replace("Dart, Deafening - ", '').replace("Dart, Electrifying - ", '').replace(
        "Dart, Panic - ", '')
    out = out.replace("Snare - ", "")
    out = out.replace("Bolt - ", '').replace("Bolt, Deafening - ", '').replace("Bolt, Electrifying - ", '').replace(
        "Bolt, Panic - ", '')
    out = out.replace("Cell, Power - ", "").replace("Cell, Cryo - ", '').replace("Cell, Deafening - ", '').replace(
        "Cell, Incendiary - ", '')

    out = out.replace("Adv. - ", "").replace("Adv. Homing - ", "").replace("Homing - ", "")
    out = out.replace("Adv. Proton - ", "").replace("Flechette - ", "").replace("Plasma - ", "").replace("Thermite - ",
                                                                                                         "")
    out = out.replace("Adv. Concussion - ", "").replace("Concussion - ", "").replace("Discord - ", "").replace(
        "Proton - ", "").replace("Silent Thunder - ", "").replace("S-Thread - ", "")

    return out


dir = 'Collections\SW5E Things\swequip gvars\weapons'
weap_out = []
filt = []

for file_name in os.listdir(dir):
    with open(os.path.join(dir, file_name)) as file:
        weapons = json.load(file)

    for weapon in weapons:
        name = processName(weapon['name'])
        ammo = weapon['name'].replace(name, '').replace(" - ", "").replace("Cell", "").replace("Bolt", "").replace("Dart", "").replace("Cartridge", "").replace("Arrow", "").replace("Rapid", "").replace("Burst", "").replace("Penetrating", "").replace("Two-Handed ", "").replace("Slug", "")
        ammo = ammo.replace("Grapple", "").replace("Rifle", "").replace("Staff", "").replace("Corruption", "").replace("Power", "").lstrip(", ")

        if name not in filt:
            filt.append(name)
            weap_out.append({"name": name, "ammo": []})
        
        weapon = next((w for w in weap_out if w['name'] == name), None)
        
        if ammo not in weapon['ammo'] and ammo != "":
            weapon['ammo'].append(ammo)

with open('Collections\SW5E Things\swequip gvars\All Weapons.json', mode='w+', encoding='utf-8') as outfile:
    outfile.write(json.dumps(weap_out))
