SW5E Condition Lookup or Application

`!swcondition "<condition>" [args]`

__Valid Arguments__

`-t [target]` - Specify any number of targets to apply the condition to.
`-l [#]` - If the condition has levels, specify the level to apply
`-dur [#]` - Duration of the condition. Default: None
`-save [str|dex|con|wis|cha|int]` - Whether the targets need to make a save first
`-dc [#]` - DC for the save. Default: 10
  
`adv` - Save is rolled at advantage
`pass` - Save is automatically passed
`dis` - Save is rolled at disadvantage
`fail` - Save is automatically failed
`end` - Use if the condition should end at the end of a turn
`caster` - Use if the effect duration should count on the caster's turn and not the targets