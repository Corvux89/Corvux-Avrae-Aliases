Add SW5e attacks to your character.

`!swequip "weapon name" [*args*]`

This will create the appropriate counter for weapons with ammunition.
Adds Burst, Rapid, and Two-Handed Attack variants for those weapons that have them.

For weapons with ammo, the format would be "Ammo type, Subtype - Weapon". Ex: "Missile, Fragmentation - Wrist Launcher"

__Available Arguments__

**General**
`-title` Rename your weapon

**To Hit**
`-b` add a bonus to your to-hit

**Damage**
`-d` add a bonus to your damage
`-c` adds extra damage when a critical hit is scored. Accepts XdY dice strings or a flat number
`-criton` allows you to set a different natural dice roll that scores a critical hit


`-noprof` removes the proficiency bonus from an attack bonus
`-offhand` removes the ability mod from your damage roll and adds an attack called "Offhand ..." for Two-Weapon Fighting
`-double` removes the ability mod from your damage roll and adds an attack called "Double ..." for Double-Weapon Fighting
`-gwm` Adds an attack called "Great..." for Great-Weapon Master. Removes the proficiency mod from the attack roll and adds double proficiency mod to the damage roll
`-sharp` Adds an attack called "Sharpshooter..." for Sharpshooter Mastery. Removes the proficiency mod from the attack roll and adds double proficiency mod to the damage roll
`-enhanced` Upgrade the damage to enhanced damage
`-gunning`
`-heavy` Sets up the weapon as if it had the heavy property
`output` returns the JSON code for the attacks so you can modify it and use `!attack import <code>` to add it manually.
*Note:* Make sure you input any desired arguments *after* the weapon name


Originally created by R to the Ichie and modified/updated by Corvux