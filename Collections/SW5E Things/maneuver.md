Maneuvers
 
`!maneuver "<maneuver>" [args]`
 
You have to have a counter named "Superiority Dice" for this to work
 
__Valid Arguments__
 
`-t [target]` - Specify any number of targets of the maneuver. Can specify adv/dis per target. ex `-t [target]|dis`
`dis` - Disadvantage on any saves
`adv` - Advantage on any saves
`pass` - Automatically pass any saves
`fail` - Automatically fail any saves
`-i` - Ignore the "Superiority Dice" requirement
`-mi [number]` - Minimum dice roll.
`-savage` - Roll 2 superiority dice and take the highest value
`crit` - Crit the die!
`-d` - Add a bonus to the dice roll
`-type [Maneuver Type]` - Used to override the maneuver type
`-dc` - Override the default maneuver DC
`-dtype` - Set the damage type if applicable

`sm` - Superiority Mastery indicator (forces the dice to be 1d4 and switches the counter)
`mm` - Maneuver Master (Adds a bonus to any superiority dice rolls, and switches the counter)
`fs` - Field Surgeon indicator. Forces the dice to max roll and then updates the counter
`max` - Will make the dice rolls be max value
`ku` - Knowledge Unbound. This will switch the die to a d4 and not alter the counter.