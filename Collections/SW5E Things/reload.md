Reload weapons
 
`!reload [weapon] [args]`
 
__Available Arguments__
`[weapon]` - Weapon name if only wanting to reload a singular weapon. Leave blank to reload all
 
`belt` - Will remove the ammo reloaded for the given weapon from a counter named "Ammo-feed belt". Will create the counter if it doesn't exist
 
`-count` - Will remove a counter from eh provided encounter. ex: `!reload revolver -count "Pouch"` will reload the revolver and remove 1 counter from a counter name pouch