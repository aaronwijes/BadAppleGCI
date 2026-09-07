# Bad Apple, but it's GCI Constellations
Grass Cutting Incremental (very good incremental, check it out) has this pretty cool feature called "Constellations".<br>
Usually, these are used to progress within the game, but they also double as a (very small) 7x7 screen!<br>
I wanted to test what I could do with said screen, hence me rendering Bad Apple on the constellation board :)

## Showcase
Watch the video here!<br>

https://github.com/user-attachments/assets/1536429c-31da-4a19-8f5a-733eba84216d

## How does this work?
The frame renderer (`main.py`) calculates the differences between two given frames to add/delete objects from the constellation board.<br>
Duplicate frames are not re-rendered.<br>

https://github.com/user-attachments/assets/baea82ec-627c-4d37-8d14-ffc2ad33b2e8

## Requirements 
- Python 3.x, preferably 3.14 since that's what I tested this code with
- All the modules in requirements.txt
- A Bad Apple video!

## Credits
@Abhimanyu8 - I'm using a modified version of their frame compiler script to generate the 7x7 frames! See the repo at https://github.com/Abhimanyu8/Bad-Apple-on-64-pixels<br>
@aaronwijes - Created the GCI constellation renderer
