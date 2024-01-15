# RollAnalyzer
**TO RESET THE INPUTS, PRESS `"resetKey"` SET IN `settings.json`**


A fully customizable application that shows you your rolling info.

This application was made for the sole purpose of analyzing your rolling style for games like **Osu!** and **ADOFAI**, showing your inaccuracy while performing constant input sequences.
The **`roll.exe`** will create `settings.json` and `keys.json` files upon first launch in the folder the executable is in. 

On this diagram you can see what most parts of the app mean.
![screenshot](https://user-images.githubusercontent.com/59146442/216723610-c4bbdabb-49fc-4219-937a-216659cdf082.jpg)

# HOW TO OVERLAY THE APP IN OBS
## Step 1: 
Create new `Window Capture` source

![capture](https://github.com/V0W4N/RollAnalyzer/assets/59146442/c587c62d-9054-4d13-9c2c-d63d2de97c1c)
## Step 2: 
Select the app

![window](https://github.com/V0W4N/RollAnalyzer/assets/59146442/cd3f4df2-9c68-44c1-bb83-e0e66a466dfc)
## Step 3:
Select `Additive` blending mode

![image](https://github.com/V0W4N/RollAnalyzer/assets/59146442/15a457fb-225d-4984-b11c-7f8661338d4b)



**`settings.json`** has many settings, most of them are explained in the file itself with comment under each setting, and other ones are intuitive enough to figure out.
Feel free to dm me on discord if you find bugs or have suggestions (i rarely check github comments but you can leave those too)
i will update it occasionally


# Updates

**Patch 1:** fixed memory leak due to raindrops not getting removed after leaving the screen (found by **dropsy#1796**)
**Patch 2:** covered up shimmer bug when keyviewer bars approach the end of the screen
***UPDATE 1:*** Changed keyboard hook library to **`keyboard`** to listen for inputs regardless of window being in focus

compiled using pyinstaller and this command:
`pyinstaller --onefile --windowed --add-data "icon32.png;." --add-data "icon.png;." --hidden-import=pygame main.py`
