for gvar_str in variable:
    gvar = load_json(get_gvar(gvar_str))
    for x in gvar:
        if help.processName(x.name).lower() == weapon.lower():
            attacks.append(x)