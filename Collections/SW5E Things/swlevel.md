Star Wars Level (swlevel)
  
Just like the `!level` we all know and love, but in space. Makes counters for Hit Dice and limited-use class features, and sets archetype in a `subclass` cvar.
 
__Supported Actions__
On top of supporting base class actions, we have implemented custom actions as well for various supported automations. To view how to setup these actions with your sheet (if you are not using the base character sheet in the collection description), or to view the list of supported actions you can check out the [document here](https://docs.google.com/spreadsheets/d/1V8BJrzt56jJNxRlx4daZayHBZJSQ7nrjNTavix2caSg/edit?usp=sharing)
  
__Basic Use__
`!swlevel` - Picks up class levels from your `character()` data.
`!swlevel <class> <archetype>` - Sets your archetype for the provided class.
`!swlevel <class> <level> [archetype]` - Sets the class levels for classes **not defined** in your `character()` data. 
`!swlevel <class>` - Removes class levels and archetype added by `!swlevel`. Cannot remove class levels pulled from your sheet.
 
__Available Arguments__
`-stat` - Overrides the stat used in the imported actions. Ex: `-stat str` 
`-update` - Will not re-create health/class counters and instead only do the supported actions section