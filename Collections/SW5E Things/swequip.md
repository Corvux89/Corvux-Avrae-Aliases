Add SW5e attacks to your character.
 
`!swequip <weapon name> [args]`
 
This will create the appropriate counter for weapons with ammunition.
Adds Burst, Rapid, and Two-Handed Attack variants for those weapons that have them.

A full list of supported weapons and ammo types can be found on the `SWEQUIP` tab of this [sheet](https://docs.google.com/spreadsheets/d/10lZrm9i6YUzuN8oNbJV77aRPeLVxe1pFRP2uqD3q3-Y/edit?usp=sharing)
 
__Available Arguments__
 
**General**
`-title` - Rename the weapon
`-noprof` - Removes the proficiency bonus from an attack bonus
`-prop` - Set the property string on a weapon
`-ammo` - Add an ammo variant on the attack. Either specify the ammo, ie. `-ammo fragmentation` or just `-ammo` will load up all the ammo variants
`-offhand` - Removes the ability mod from the damage roll and adds an attack called "Offhand ..." for Two-Weapon Fighting
`-double` - Removes the ability mod from the damage roll and adds an attack called "Double ..." for Double-Weapon Fighting
`-f` - Adds a description field. If the weapon has a property text, all fields defined here will be added before
`-dc` - Override the DC of saves/checks in the automation
 
**To Hit**
`-b` - Add a bonus to the to-hit roll
`-bstat` - Will swap out the modifier used for the to-hit roll. Ex: `-bstat wis` will swap the current weapons to-hit stat to the characters wisdom modifier
  
**Damage**
`-dmg` - Change the damage die on the attack
`-d` - Add a bonus to the damage
`-dtype` - Change the damage type to the provided type
`-ad` - Add a bonus damage with a different damage type. Ex: `-ad 1d4 [force]`
`-c` - Adds extra damage when a critical hit is scored. Accepts XdY dice strings or a flat number
`-criton` - Allows a different natural dice roll that scores a critical hit
`-keen` - Set a different natural dice roll scoring a critical hit (20 - keen). Same as `-criton` just different math
`-enhanced` - Upgrade the damage to `enhanced` damage
`-dstat` - Will swap out the modifier used for the damage roll. Ex: `-dstat wis` will swap the current weapons damage stat to the characters wisdom modifier
 
**Properties**
`-biting` - Sets up the weapon as if it had the biting property
`-bright` - Sets up the weapon as if it had the bright property
`-burst` - Sets up the weapon as if it had the burst property
`-corruption` - Sets up the weapon as if it had the corruption property
`-disarming` - Sets up the weapon as if it had the disarming property
`-disintegrate` - Sets up the weapon as if it had the disintegrate property
`-disruptive` - Sets up the weapon as if it had the disruptive property
`-finesse` or `-mighty` - Replaces the stat used for rolls with either strength or dexterity (whichever is higher)
`-heavy` - Sets up the weapon as if it had the heavy property
`-igniting` - Sets up the weapon as if it had the igniting property
`-neuralizing` - Sets up the weapon as if it had the neuralizing property
`-penetrating` - Sets up the weapon as if it had the penetrating property
`-reload` - Set or override a reload amount for the weapon
`-rapid` - Sets up the weapon as if it had the rapid property
`-shocking` - Sets up the weapon as if it had the shocking property
`-sonorous` - Sets up the weapon as if it had the sonorous property
`-staggering` - Sets up the weapon as if it had the staggering property
`-vicious` - - Sets up the weapon as if it had the vicious property
 
**Feats**
`-gwm` - Adds an attack called "Great..." for Great-Weapon Master. Removes the proficiency mod from the attack roll and adds double proficiency mod to the damage roll
`-sharp` - Adds an attack called "Sharpshooter..." for Sharpshooter Mastery. Removes the proficiency mod from the attack roll and adds double proficiency mod to the damage roll
`-gunning` Sets up the weapon for Gunning Mastery
`-gunmas` - Adds an attack called "Gunning..."for Gunning Mastery. Removes the proficiency bonus from teh attack roll and updates the damage as appropriate
`-gunstyle` - Adds an attack called "Gunning..."for Gunning Style. 

**Misc**
`-byrad` - Adds an attack for the Byrothsis Adept Lightweapon
`-byran` - Adds an attack for the Byrothsis Ancient Lightweapon
 
**Extras**
`output` returns the JSON code for the attacks so you can modify it and use `!attack import <code>` to add it manually.
 
*Note:* Make sure you input any desired arguments *after* the weapon name
 
Originally created by R to the Ichie and modified/updated by Corvux