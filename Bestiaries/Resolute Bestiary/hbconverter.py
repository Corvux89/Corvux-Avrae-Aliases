import json

def get_value(monster, key, default):
    value = monster.get(key, default)
    return value if value != "" else default

def format_actions(actions, title):
    if not actions:
        return ""
    actions_text = "\n:\n".join([f"***{action['name']}.*** {action['description']}" for action in actions])
    return f"### {title}\n{actions_text}\n:\n"

def format_monster(monster):
    ## Can make this conditional later
    frame = "{{monster,frame,wide"

    # Basic monster info
    name = get_value(monster, "name", "Unknown Monster")
    size = get_value(monster, "size", "Unknown Size")
    type_ = get_value(monster, "race", "Unknown Type")
    alignment = get_value(monster, "alignment", "Unknown Alignment")
    ac = get_value(monster, "ac", "Unknown AC")
    armor_type = get_value(monster, "armortype", None)
    hp = get_value(monster, "hp", "Unknown HP")
    hitdice = get_value(monster, "hitdice", "Unknown Hitdie")
    speed = get_value(monster, "speed", "Unknown Speed")
    image = get_value(monster, "image_url", None)
    
    # Format Image
    image_str = f"![{name}]({image}){{float:right;width:100px}}" if image else ""

    # Stats
    stats = monster.get("ability_scores", {})
    stat_line = "|  STR  |  DEX  |  CON  |  INT  |  WIS  |  CHA  |\n"
    stat_line += "|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|\n"
    stat_line += "|{} ({:+})|{} ({:+})|{} ({:+})|{} ({:+})|{} ({:+})|{} ({:+})|".format(
        stats.get("strength", 10), (stats.get("strength", 10) - 10) // 2,
        stats.get("dexterity", 10), (stats.get("dexterity", 10) - 10) // 2,
        stats.get("constitution", 10), (stats.get("constitution", 10) - 10) // 2,
        stats.get("intelligence", 10), (stats.get("intelligence", 10) - 10) // 2,
        stats.get("wisdom", 10), (stats.get("wisdom", 10) - 10) // 2,
        stats.get("charisma", 10), (stats.get("charisma", 10) - 10) // 2,
    )

    # Additional attributes
    saves = monster.get('saves', {})
    save_str = ", ".join(
        f"{k[:3].capitalize()} +{v.get('value')}"
        for k, v in saves.items()
        if v.get('prof', 0) > 0 or v.get('value') != (stats.get(k.replace('Save',''), 10) - 10) // 2
    )

    skills = monster.get('skills', {})
    skill_str = ", ".join(
        f"{k.capitalize()} +{v.get('value')}"
        for k, v in skills.items()
        if v.get('prof', 0) > 0
    )

    condition_immunities = monster.get("condition_immune", [])
    vulnerabilities = monster.get("vulnerabilities", [])
    resistances = monster.get("resistances", [])
    senses = get_value(monster, "senses", "None")
    passive_perception = get_value(monster, "passiveperc", None)
    senses += f", Passive Perception {passive_perception}" if passive_perception else ""
    languages = monster.get("languages", [])
    challenge = get_value(monster, "cr", "Unknown Challenge")
    xp = get_value(monster, "xp", 0)
    proficiency_bonus = stats.get("prof_bonus", "+0")

    attr_str = "\n".join(filter(None, [
        f"**Saving Throws** :: {save_str}" if save_str else None,
        f"**Skills** :: {skill_str}" if skill_str else None,
        f"**Condition Immunities** :: {', '.join(condition_immunities)}" if condition_immunities else None,
        f"**Vulnerabilities** :: {', '.join(vulnerabilities)}" if vulnerabilities else None,
        f"**Resistances** :: {', '.join(resistances)}" if resistances else None,
        f"**Senses** :: {senses}",
        f"**Languages** :: {', '.join(languages) if languages else 'None'}",
        f"**Challenge** :: {challenge} ({xp} XP) {{{{bonus **Proficiency Bonus** {proficiency_bonus}}}}}"
    ]))

    # Traits
    traits = monster.get("traits", [])
    # Preprocess the traits list because spellcasting is weird
    processed_traits = []
    for trait in traits:
        description = trait['description']
        if trait['name'] == "Spellcasting" or trait['name'] == "Innate Spellcasting":
            # Replace single newlines with double newlines for "Spellcasting"
            description = description.replace("\n", "\n\n")
        processed_traits.append(f"***{trait['name']}.*** {description}")


    traits_text = "\n:\n".join(processed_traits)

    # Daily Spells
    spellcasting = monster.get('spellcasting', {})
    known_spells = spellcasting.get("known_spells", {})
    daily_spells = known_spells.get('daily_spells', {})
    spell_str = None
    for l, s in daily_spells.items():
        if s:
            if not spell_str:
                spell_str = f"{l}/day: *{', '.join(s)}*"
            else:
                spell_str += f"\n{l}/day: *{', '.join(s)}*"


    # Actions, Bonus Actions, Reactions, Legendary Actions
    actions_text = format_actions(monster.get("actions", []), "Actions")
    bonus_actions_text = format_actions(monster.get("bonus_actions", []), "Bonus Actions")
    reactions_text = format_actions(monster.get("reactions", []), "Reactions")
    legendary_actions_text = format_actions(monster.get("legactions", []), "Legendary Actions")

    # Combine everything into the Homebrewery format
    markdown = f"""
{frame}
## {name}
*{size} {type_}, {alignment}*

{image_str}
___
**Armor Class** :: {ac}{f" ({armor_type})" if armor_type else ""}
**Hit Points**  :: {hp} ({hitdice.replace(' ', '')})
**Speed**       :: {speed}
___
{stat_line}
___
{attr_str}
___
{traits_text}
{spell_str if spell_str else ''}
{actions_text}
{bonus_actions_text}
{reactions_text}
{legendary_actions_text}
}}}}
{{{{pageNumber,auto}}}}
\page
"""
    return markdown.strip()

def convert_json_to_markdown(json_file, output_file):
    # Read the JSON file
    with open(json_file, "r") as file:
        monsters = json.load(file)

    # Convert each monster to markdown
    markdown_list = [format_monster(monster) for monster in monsters]

    # Write the markdown to the output file
    with open(output_file, "w") as file:
        file.write("\n\n".join(markdown_list))

# Example usage
convert_json_to_markdown("Bestiaries/Resolute Bestiary/Resolute Ground.json", "Bestiaries/Resolute Bestiary/output.md")