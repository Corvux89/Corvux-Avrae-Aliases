**Cast Powers using Force or Tech Points**

Use `!power "Power Name"` to cast a power using either Force or Tech Points. This requires a counter named "Force Points" or "Tech Points" and the power must be in your spellbook (or use `-i` to ignore requirements). This uses `!cast` as a base command, so it accepts any argument that `!help cast` lists as available.  You may modify the points cost without changing the level of the power by using `-p #`.

__Available Arguments__
All arguments for `!cast` work with `!power`, but here are some specific ones we also will use:

`-i` - Ignore the power costs
`with <stat>` - Use a different casting stat
`-p #` - Override the cost amount
`-cc <counter name` - Manually override the custom counter to use

## Class/Subclass Support
If you want to use the spellbook version of a spell below and not the class version use the `base` argument and it will ignore the class specific versions. 

#### Fighter
`Adept Specialist` - Support for Growing Momentum

### Monk
`Vow of the Devoted` - Will switch cost and counter to Focus points. If character is multiclassed with a class that has Force Points, then use the `focus` argument to switch to Focus Points as Force Points will be prioritized

#### Scout
`Bulwark` - Support for Personal Barrier

#### Sentinel

`Path of Meditation` - Will switch Guidance, Battle Meditation, Improved Battle Meditation, and Master Battle Meditaiton to a subclass specific automation

`Ideal of the Tranquil` - Will switch to use Tranquil force points first, and then overlow to Force Points


## Feature Support
If you are a Tech/Force caster and want to use your Tech/Force points instead of the feat counters, use the `` argument and it will ignore the feat counters.

`Tech Dabbler`
`Force Sensitive`

Made by Corvux#5222