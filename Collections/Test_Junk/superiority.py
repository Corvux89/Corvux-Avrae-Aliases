
def get_bonus(m):
    s = character().stats
    m_mod = max(s.get_mod("wisdom"), s.get_mod("intelligence"), s.get_mod("charisma"), 0)
    p_mod = max(s.get_mod("strength"), s.get_mod("dexterity"), s.get_mod("constitution"), 0)
    if m.sub == "Mental":
        return m_mod
    elif m.sub == "Physical":
        return p_mod
    else:
        return max(m_mod, p_mod)
def heal(roll_str, coms):
    roll = vroll(roll_str)
    if len(coms)>0:
        for c in coms:
            c.modify_hp(roll.total, overflow=False)

    return roll
