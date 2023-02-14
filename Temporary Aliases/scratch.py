import binascii
import random
import string


def test(base: str):
    abbreviation = "TF1234"

    base_str = base[:4]

    if len(base_str) < 4:
        base_str+= "".join(random.choices(string.ascii_letters, k=(4-len(base_str))))

    base_str = binascii.hexlify(bytes(base_str, encoding='utf-8'))

    base_str = base_str.decode("utf-8")

    transponder = f"{abbreviation}_{base_str}_BD:1"
    print(f'{transponder}')



def get_bonus(m, override = None):
    s = character().stats
    m_mod = max(s.get_mod("wisdom"), s.get_mod("intelligence"), s.get_mod("charisma"), 0)
    p_mod = max(s.get_mod("strength"), s.get_mod("dexterity"), s.get_mod("constitution"), 0)

    if (m.sub == "Mental" and not override) or (override and  'men' in override.lower()):
        return m_mod
    elif (m.sub == "Physical" and not override) or (override and 'phy' in override.lower()):
        return p_mod
    elif override and 'gen' in override.lower():
        return max(m_mod, p_mod)
    else:
        return max(m_mod, p_mod)

def get_roll_str(m, cc, mi, override = None):
    lvl = character().get_cc_max(cc)
    out_str = "1d12" if lvl > 10 else "1d10" if lvl > 8 else "1d8" if lvl > 6 else "1d6" if lvl > 4 else "1d4"

    if mi:
        out_str += f'mi{mi}'

    if m.apply_mod:
        out_str += f'+ {get_bonus(m, override)}'

    return out_str

def add_effect(m, com, override=None):
    output = ""
    peff = ""
    for e in m.effect:
        for p in combat().me.effects:
            if p.name == e.name:
                peff = p
                break

        if peff == "":
            peff = combat().me.add_effect(e.name, duration=e.get('duration'),  end=True if e.get('end') else False)

        description = e.get('description') if not None else ''
        if "mod" in description.lower():
            description += f"\n -Modifier: {get_bonus(m, override)}"
        com.add_effect(e.name, desc=f"{description}\n -[Source: {character().name}]",
                       end=True if e.get('end') else False, passive_effects=e.get('p_effect'), parent=peff)

        output += f"**Effect:** {e.name} {'['+e.get('duration')+' rounds]' if e.get('duration') else ''}\n"

    return output

# I hate this function..I'll eventually make it better but it works for now
def calc_damage(m, damage, com):
    f_str = ""
    if m.d_type != "":
        if com.resistances.is_immune(m.d_type):
            f_str += f"{damage.total} * 0 [{m.d_type}] = `0`\n"
        elif com.resistances.is_resistant(m.d_type):
            d = floor(damage.total / 2)
            f_str += f"{damage.total} / 2 [{m.d_type}] = `{d}`\n"
            com.modify_hp(-d)
        elif com.resistances.is_vulnerable(m.d_type):
            d = floor(damage.total * 2)
            f_str += f"{damage.total} * 2 [{m.d_type}] = `{d}`\n"
            com.modify_hp(-d)
        else:
            f_str += f"{damage.total} [{m.d_type}] = `{damage.total}`\n"
            com.modify_hp(-damage.total)
    else:
        com.modify_hp(-damage.total)
        f_str += f"'{damage.total}\n'"

    return f_str


def perform(m, coms, roll_str, dc, fail, override = None):
    output = ""
    if m.type in  ["Heal", "T_Heal"]:
        heal = vroll(roll_str)
        if m.type == "Heal":
            output += f''' -f "Meta|{heal} [healing]" '''
        else:
            output += f''' -f "Meta|{heal} [temp healing]" '''

        if len(coms) > 0:
            for com in coms:
                f_str = f"{com.hp} + {heal.total} [healing]\n"
                if m.effect:
                    f_str += add_effect(m, com, override)
                output += f''' -f "{com.name}|{f_str}" '''

                if m.type == "Heal":
                    com.modify_hp(heal.total, overflow=False)
                elif m.type == "T_Heal":
                    com.set_temp_hp(heal.total)

    if m.save:
        m_str=""
        if m.type in ["Damage", "Add_Damage"]:
            damage = vroll(roll_str)
            m_str += f"**Damage:** {damage} {m.d_type}\n"

        if m.type == "Check":
            for (n, s) in character().skills:
                if n.lower() == m.c_type.lower():
                    skill = s
                    break
            if skill.adv:
                    r_str = f"2d20kh1 + {skill.value}"
            else:
                r_str = f"1d20 + {skill.value}"
            if m.apply_mod:
                r_str += f'+ {get_bonus(m, override)}'

            ch = vroll(r_str)
            m_str += f"**{m.c_type} save DC:** {ch}\n"
            dc = ch.total
        else:
            m_str += f"**{m.save} save DC:** {dc}\n"

        if m.type == "Roll":
            m_str += f"**Roll:** {vroll(roll_str)}\n"
        elif m.type == "Mod":
            m_str += f"**{m.sub} Mod:** {get_bonus(m, override)}\n"

        output += f''' -f "Meta|{m_str}" '''

        if len(coms)>0:
            for com in coms:
                s = com.save(m.save)

                if m.type == "Add_Damage":
                    f_str = "**Damage:** "
                    f_str += calc_damage(m, damage, com)

                if s.total < dc or fail:
                    f_str = f"{s}; *Failure!*\n"
                    if m.type == "Damage":
                        f_str += "**Damage:** "
                        f_str += calc_damage(m, damage, com)

                    if m.effect:
                        f_str += add_effect(m, com, override)

                    output += f''' -f "{com.name}|{f_str}" '''

                else:
                    output += f''' -f "{com.name}|{s}; **Success!**" '''
    else:
        if m.type == "Damage":
            damage = vroll(roll_str)
            if m.d_type:
                output += f''' -f "Meta|**Damage:** {damage} [{m.d_type}]" '''
            else:
                output += f''' -f "Meta|**Damage:** {damage}" '''

        elif m.type == "Roll":
            output += f''' -f "Meta|**Roll:** {vroll(roll_str)}" '''
        elif m.type == "Mod":
            output += f''' -f "Meta|**{m.sub} Mod:** {get_bonus(m)}" '''

        if len(coms)>0:
            for com in coms:
                f_str = ""
                if m.type in ["Damage", "Add_Damage"]:
                    f_str += f"**Damage:** {calc_damage(m, damage, com)}"

                if m.effect and m.type not in ["Heal", "T_Heal"]:
                    f_str += add_effect(m, com, override)

                if f_str != "":
                    output += f''' -f "{com.name}|{f_str}" '''

    return output
