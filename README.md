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
Select `Filters` then add `Color key` filter

![image](https://github.com/V0W4N/RollAnalyzer/assets/59146442/a6225676-2466-4255-b994-e812b8f8efd7)

![image](https://github.com/V0W4N/RollAnalyzer/assets/59146442/8995b959-a494-47f9-b69d-d852a0e9d7b8)


## Step 4:
Put these settings in, and play around with `Smoothness` to get the fade look like you want it to

![image](https://github.com/V0W4N/RollAnalyzer/assets/59146442/0956cb4a-09c3-418c-85fa-3482098c01ce)


**`settings.json`** has many settings, most of them are explained in the file itself with comment under each setting, and other ones are intuitive enough to figure out.
Feel free to dm me on discord if you find bugs or have suggestions (i rarely check github comments but you can leave those too)
i will update it occasionally


# Updates

**Patch 1:** fixed memory leak due to raindrops not getting removed after leaving the screen (found by **dropsy#1796**)

**Patch 2:** covered up shimmer bug when keyviewer bars approach the end of the screen

**Patch 3:** fixed list indexing error when setting keys (found by **senatorial**)

***UPDATE 1:*** Changed keyboard hook library to **`keyboard`** to listen for inputs regardless of window being in focus

compiled using pyinstaller
