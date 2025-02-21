# CrossCode World Randomizer  

This mod randomizes all locations in CrossCode.  

## Features  
- Randomizes all locations in the game (zones, doors).  
- Simple interface: select the game's map folder, choose your options, and click "Randomize."  
- Customizable settings for different playstyles (randomized enemies, unique enemies, bosses).  

## Installation  
1. Download the latest release from [GitHub Releases](https://github.com/Atsouky/cc-WorldRandomizer/releases/tag/v0.7.4).  
2. Put the files into a folder of your choice.  
3. Run the application (`Randomize.exe`).  

 

## ⚠ Disclaimer ⚠

This software has been packaged using **PyInstaller**, which may cause some antivirus programs to flag it as a potential threat.  

###  Why is this happening?
- Certain antivirus programs may mistakenly flag **PyInstaller** executables as threats.
- The application **does not contain any malicious code**.
- You can verify this by checking a **ViruScanner** or reviewing the **source code**.

### How to proceed safely:
1. If Windows Defender blocks the file, click **"More info" > "Run anyway"**.
2. You can **add the file to your antivirus exceptions** if needed.
3. If you have concerns, you can run the **source code version** instead of the executable. (Python needed with matplotlib and neworkx)
4. Or simply wait until the version is known by Microsoft (Too long or need money for a certificate)

### 🔗 Additional Information
- [VirusScanner](https://internxt.com/virus-scanner) 
- [Source Code](https://github.com/Atsouky/cc-WorldRandomizer/blob/main/Randomize.py)

Thank you for your trust! 

## Usage 

1. Open the application.  
2. Select your CrossCode maps folder (`.../CrossCode/assets/data/maps`).  
3. Choose the randomization options you want.  
4. Click the "Randomize" button.  
5. A folder named `World_Rando_mods_{seed}` will be created in your folder.
6. Place the `World_Rando_mods_{seed}` folder into your mods folder
7. Launch CrossCode and ensure the mod is enabled in the options.  

## Notes  
- The tutorial is not randomized because of all ablilities has not been unlock yet so it start at rookie harbor
- If you want the spoiler file, you can find it in `World_Rando_mods_{seed}/spoiler/spoiler.txt`.  
- Back up your original game files before using the randomizer.  
- If you encounter issues, restore your original maps from your backup.  

> **PS:** I'm French, so sorry if my English isn't perfect!  

## Known Issues  
- Only level 1 height is randomized because some maps (e.g., `guilde.entrance` has, like, *8* teleporters, 5 of which are inaccessible) contain multiple `TeleporterGround`, leading to unreachable areas.  
- Some `TeleporterGround` are used for developer debugging, which can teleport players into the void or the ground (e.g., in `autumn.path6` in the wall).  
- There may be errors when linking maps; they will be listed in `World_Rando_mods_{seed}/spoiler/unstable_link.txt`.  
- Randomizing enemies works fine, but randomizing bosses or unique enemies can cause softlocks due to enemy dependencies or invulnerable enemies.  

