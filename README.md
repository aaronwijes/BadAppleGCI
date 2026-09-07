# Bad Apple, but it's GCI Constellations
Grass Cutting Incremental (very good incremental, check it out) has this pretty cool feature called "Constellations".<br>
Usually, these are used to progress within the game, but they also double as a (very small) 7x7 screen!<br>
I wanted to test what I could do with said screen, hence me rendering Bad Apple on the constellation board :)

## Showcase
Watch the video here!<br><br>
<video src="./videos/bad_apple_gci.mp4" alt="Bad Apple on GCI Constellations" width="300"/>

## How does this work?
The frame renderer (`main.py`) calculates the differences between two given frames to add/delete objects from the constellation board.<br>
Duplicate frames are not re-rendered.<br>

<video src="./videos/frame_renderer.mp4" alt="Constellation Frame Renderer" width="300"/>

## Requirements 
- Python 3.x, preferably 3.14 since that's what I tested this code with
- All the modules in requirements.txt
- A Bad Apple video!

## Credits
@Abhimanyu8 - I'm using a modified version of their frame compiler script to generate the 7x7 frames! See the repo at https://github.com/Abhimanyu8/Bad-Apple-on-64-pixels<br>
@aaronwijes - Created the GCI constellation renderer