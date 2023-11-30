# New SWEQUIP Module

ch = character()

def processAttacks(args):
    out = []
    type = None

    if len(args) == 0:
        return err("Need to specify a weapon type")
    elif len(args) >1 and "-" not in args[0]:
        type = args[0]

