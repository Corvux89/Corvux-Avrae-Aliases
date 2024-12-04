# NEW SWEQUIP Primary Module

c = character()
feats = load_json(c.get_cvar("SWFeats", "{}"))
using(weap="8202f283-16d2-47ba-8a5e-0d0cf29a1ef1", sup="8b78365a-5c05-4c8f-8364-fbde2e3de862", primary="df07d6ae-140d-45b1-b026-de831064acab")
stats = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
ammo = load_json(get_gvar("77d6f3c7-65c9-467b-b019-a833c1e7a852"))
subclasses = sup.get_subclasses()

def processAttacks(attacks, args):
    out = []

    for i, weapon in enumerate(attacks):
        counter = ""
        attack = {}
        props = [p.lower() for p in weapon.properties] if 'properties' in weapon else []
        prop = " ".join(props)
        attackStat = "max(strengthMod,dexterityMod)" if "finesse" in props or "mighty" in props else "strengthMod" if weapon.type.lower() == "melee" else "dexterityMod" 
        name = weapon.name

        # Build the weapon(s)        
        effects = []
        damage = damage_string(f"{weapon.damage_die}+{{{attackStat}}} [{weapon.damage_type}]")
        effects.append(attack_string(f"proficiencyBonus+{attackStat}", [damage]))

        # Reload
        if "reload" in prop:
            effects.append(counter_string(weapon.name, 1))

        # Ammo
        if 'ammo' in weapon and args.get('ammo'):
            if ammo_type := ammo.get(weapon.ammo):
                if auto := ammo_type.get(args.last('ammo').lower()):
                    name = f"{ammo_type.title}, {auto.title} - {name}"
                    effects+=auto.automation
                else:
                    types = ammo_type.keys()
                    ammo_str = "\n".join([t.capitalize() for t in types if t != 'title'])
                    return err(f"Unsure of ammo type `{args.last('ammo')}`.\n**Available Options:**\n{ammo_str}")    
            else:
                return err(f"Unsure of ammo type `{weapon.ammo}`. This should be reported.")

        target = {"type": "target", "target": "each", "effects": effects}
        text = {"type": "text", "text": f"{', '.join(weapon.properties)}"}

        # Base Weapon        
        a = {"name": f"{name}", "_v": 2, "automation": [target, text]}
        attack = dump_json(a)

        if 'auto' not in props:
            out.append(a)

        # Variants
        if 'rapid' in prop:
            r = int(prop[prop.index("rapid "):].lstrip("rapid ")[:2].rstrip(", "))
            args.update({"rapid": r})

        if 'burst' in prop:
            b = int(prop[prop.index("burst "):].lstrip("burst ")[:2].rstrip(", "))
            args.update({"burst": b})
    
    return primary.processAttacks(out, args)

def damage_string(damage_str, fixedValue = False):
    return {
        "type": "damage",
        "damage": f"{damage_str}",
        "fixedValue": fixedValue
    }

def attack_string(attackBonus, hit = [], miss = [], adv = 0):
    return { 
        "type": "attack",
        "attackBonus": f"{attackBonus}",
        "hit": hit,
        "miss": miss,
        "adv": adv
    }

def counter_string(counter, amount):
    return {
        "type": "counter",
        "counter": f"{counter}",
        "amount": f"{amount}",
        "errorBehaviour": "raise",
        "allowOverflow": False
    }