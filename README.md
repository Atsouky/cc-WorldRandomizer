# CrossCode World Randomizer  

This mod randomizes all locations in CrossCode.  

## Features  
- Randomizes all locations in the game (zones, doors).  
- Simple interface: select the game's map folder, choose your options, and click "Randomize."  
- Customizable settings for different playstyles (randomized enemies, unique enemies, bosses).  

## Installation  
1. Download the latest release from [GitHub Releases](https://github.com/Atsouky/cc-WorldRandomizer/releases/tag/v0.7.3).  
2. Put the files into a folder of your choice.  
3. Run the application (`Randomize.exe`).  

## Usage  
1. Open the application.  
2. Select your CrossCode maps folder (`.../CrossCode/assets/data/maps`).  
3. Choose the randomization options you want.  
4. Click the "Randomize" button.  
5. A folder named `World_Rando_mods_{seed}` will be created in your folder.
6. Place the `World_Rando_mods_{seed}` folder into your mods folder
7. Launch CrossCode and ensure the mod is active in the options.  

## Notes  
- The tutorial is not randomize because of all ablilities not been unlock yet so it start at rookie harbor
- If you want the spoiler file, you can find it in `World_Rando_mods_{seed}/spoiler/spoiler.txt`.  
- Back up your original game files before using the randomizer.  
- If you experience issues, you can restore the original maps using your backup.  

> **PS:** I'm French, so sorry if my English isn't perfect!  

## Known Issues  
- Only level 1 height is randomized because some maps (e.g., `guilde.entrance` like *8* teleporters, 5 of which are inaccessible) contain multiple `TeleporterGround`, leading to unreachable areas.  
- Some `TeleporterGround` are used for developer debugging, which can teleport players into the void or the ground (e.g., in `autumn.path6` in the wall).  
- There may be errors when linking maps; they will be listed in `World_Rando_mods_{seed}/spoiler/unstable_link.txt`.  
- Randomizing enemies works fine, but randomizing bosses or unique enemies can cause softlocks due to enemy dependencies or invulnerable enemies.  

