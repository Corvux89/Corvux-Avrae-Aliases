**Cast Tech Powers using Tech Points**

Use `!tpcast "Power Name"` to cast a power using Tech Points.  This requires a counter named "Tech Points" and the power must be in your spellbook (or use `-i` to ignore requirements). This uses `!cast` as a base command, so it accepts any argument that `!help cast` lists as available.  You may modify the points cost without changing the level of the power by using `-p #`.

 **Want to add Homebrew powers?**
Start by putting your powers in a tome on the [Avrae Dashboard](https://avrae.io/dashboard/homebrew/spells).  Export that tome to JSON and copy it to a new gvar.  You can remove everything except name and level of each power to save space if you need to.  Take the address of that gvar and put it in a `uvar` called `brewspells`, formatted as a list (i.e. `!uvar brewspells ["01a1a2e8-6167-4bda-a513-45cfa56b26d4"]`, separating each address with a comma).  You can also make a tome available to a server by creating a server variable (`svar`) called `brewspells`, following the same format.

Created by R to the Ichie and updated by Corvux