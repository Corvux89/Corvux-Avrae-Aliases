<drac2>
ch = character()
try:
    level = int(&ARGS&[0])
except:
    return err(f"Use this like `{ctx.prefix}tfix 3` to swap out the `Tech Dabbler - 3` slot for a 3rd level power slot")

if ch.cc_exists(f"Tech Dabbler - {level}"):
    ch.mod_cc(f"Tech Dabbler - {level}", +1)

    if ch.cc_exists("Tech Points"):
        ch.mod_cc("Tech Points", -(level+1))
    return f'''embed -title "{ch.name} fixes their counters" -desc "Corvux was too lazy to figure this out with `!power` so made a separate thing just for him" -f "Tech Dabbler - {level} (+1)|{ch.cc_str(f'Tech Dabbler - {level}')}" -f "Tech Points (-{level+1})|{ch.cc_str("Tech Points")}" -footer "God he's the worst....boo that man" -image "https://cdn.discordapp.com/attachments/987038574245474304/1364350005439103129/DgKiqcRX4AUMnyn.png?ex=68095975&is=680807f5&hm=f0a2d6bfbb2a596a632fb8166acc4c7bab7946d242d09931d2f47d9a7c341c35&"'''

return err("Nope...not happenin")
</drac2>