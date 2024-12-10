Aliases and snippets for the Resolute SW5E server. This is an active work in progress for the Resolute SW5E server.

Some of this are updates of R to the Ichie's work, some of this is my own work. 

You can view the source code for these (plus some of my scratch work) on my [GitHub](https://github.com/Corvux89/Corvux-Avrae-Aliases).

If you like what i'm doing you can buy me a coffee on [Ko-Fi](https://ko-fi.com/corvux).

If you see an issue, or have a request of something you would like added you can either do a PR to the repo, or contact me on discord

__Setup__
Using the adapted SW5E Character sheet, [link here if you don't have it](https://docs.google.com/spreadsheets/d/17majk3zixwQguF8AqsS2ZfgLm4neZaimq9vmjwniuBw/edit#gid=359784640), import in, using `!import <url>`
 
After importing run `!swlevel` to setup your levels, and hit die, and any customizations as defined via our [action spreadsheet](https://docs.google.com/spreadsheets/d/1V8BJrzt56jJNxRlx4daZayHBZJSQ7nrjNTavix2caSg/edit?usp=sharing). Refer to those command help texts for any specifics on running them, but this should cover your base setup. `!swequip` will help setup weapons and counters.

 
[Spell Tome](https://avrae.io/homebrew/spells/60f243f60dc83c7c1d3a37cc)
[Racecast Tome](https://avrae.io/homebrew/spells/63f6250d10480b313f4ee666)

__Server Customization Options__
# Server Variable: sw5e
`!svar sw5e {}`

Example:
`!svar sw5e {"castMod": "wis"}`

## castMod
Can be set using `!swconfig castStat` to override the casting stat used in `power`. This will set all powers to be cast using this stat.
This would be a `str` of the casting abbreviation.
##  levels
An array of GVAR's for custom class GVARs
## actions
An array of GVAR's for custom additional actions
## race
An array of GVAR's for custom species
## spells
An array of GVAR's for custom spell overrides. This is used if an archetype has modified version of a spell


