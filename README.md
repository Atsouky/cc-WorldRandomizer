# CrossCode World Randomizer

This mod randomizes all locations in Croscode.

## Features
- Randomizes all locations in the game (zone, doors).
- Simple interface: select the game's maps folder, choose your options, and click "Randomize".
- Customizable settings for different playstyles (random : enemies, unique enemies, bosses ).

## Installation
1. Download the latest release from [GitHub Releases](https://github.com/Atsouky/cc-WorldRandomizer/releases/tag/v0.7.2).
2. Put the files into a folder of your choice.
3. Run the application (`Randomize.exe`).

## Usage
1. Open the application.
2. Select your CrossCode maps folder. (`.../Crosscode/assets/data/maps`)
3. Choose the randomization options you want.
4. Click the **Randomize** button.
5. It will create a folder like `World_Rando_mods_{seed}` and put it in you mods folder
7. Launch CrossCode and enjoy the randomized world! (and verify in opition if it is active)

## Notes
- If you want the spoiler it is in the `World_Rando_mods_{seed}/spolier/spoiler.txt` file
- Back up your original game files before using the randomizer.
- If you experience any issues, you can restore the original maps by replacing them with your backup.
- PS : I'm French, so sorry for my poor English

## Bugs
- Only level 1 height randomize (because i don't who da f*ck put 8 TeleporterGround in the guilde.entrance maps and i think this is not isolated (unreachable Teleporter Ground))
- And there is TeleporterGround use for developper debugging, so we teleporte into the void or the ground (there is one in autumn.path6)
- There is some error when linking maps it will be listed in the `World_Rando_mods_{seed}/spolier/unstable_link.txt` file
- If you randomize enemies, no problem. But if you randomize bosses or unique enemies, it will mainly result in softlocks by enemies that require other enemies to beat or immortal enemies.
