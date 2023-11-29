# New SWEQUIP Module

ch = character()

def processAttacks(attacks, args):
    out = []

    for i, a in enumerate(attacks):
        weapon_name = a.get("name") if not args.get("name") else args.last("name")
        num_die = a.get("damageNumberOfDice") if not args.get("numDie") else args.last("numDie")
        die_size =
        return err(a)