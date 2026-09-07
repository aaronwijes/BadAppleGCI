import pyautogui
import json
import time
import mss
import mss.tools
import os
import shutil

def take_ss(frame):
    with mss.MSS() as sct:
        region = {"left": 929, "top": 199, "width": 535, "height": 526}
        output = f"./screenshots/frame_{frame}.png"
        sct_img = sct.grab(region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

if not os.path.exists("./screenshots/"):
    os.makedirs("./screenshots/")

frames = json.loads(open("frames.json", "r").read())
cache = json.loads(open("cache.json").read())
frame_dir_files = os.listdir("./screenshots/")

def diff_grid(frame_1, frame_2):
    diffed_grid = {}
    for y in range(7):
        diffed_grid[y] = []
        for x in range(7):
            if frame_1[y][x] == 0 and frame_2[y][x] == 1:
                diffed_grid[y].append(1)
            elif frame_1[y][x] == 1 and frame_2[y][x] == 0:
                diffed_grid[y].append(0)
            else:
                diffed_grid[y].append(None)
    return diffed_grid

def color_all_grid():
    for a, row in enumerate(frame, start=0):
        if row != [0, 0, 0, 0, 0, 0, 0]:
            for b, block in enumerate(row, start=0):
                if block == 1:
                    pyautogui.click(pos_grid[a][b], _pause=False)
                    time.sleep(0.05)

def fill_needed(diffed_grid):
    for row in diffed_grid.values():
        for entry in row:
            if entry == 1:
                return True

def delete_needed(diffed_grid):
    for row in diffed_grid.values():
        for entry in row:
            if entry == 0:
                return True

def color_diffed_grid(diffed_grid):
    print(diffed_grid)
    pyautogui.moveTo(first_const, _pause=False)

    if fill_needed(diffed_grid):
        for y, row in enumerate(diffed_grid.values()):
            for x, entry in enumerate(row):
                if entry == 1:
                    pyautogui.click(pos_grid[y][x], _pause=False)
                    pyautogui.click(pos_grid[y][x], _pause=False)
                    time.sleep(0.05)

        time.sleep(0.05)

    if delete_needed(diffed_grid):
        pyautogui.click(deletetoggle)
        time.sleep(0.05)
        for y, row in enumerate(diffed_grid.values()):
            for x, entry in enumerate(row):
                if entry == 0:
                    pyautogui.click(pos_grid[y][x], _pause=False)
                    pyautogui.click(pos_grid[y][x], _pause=False)
                    time.sleep(0.05)
        pyautogui.click(deletetoggle)
        time.sleep(0.05)

# use this code in a python shell to get current mouse position:
# import time,pyautogui;time.sleep(3);print(pyautogui.position())
pyautogui.DARWIN_CATCH_UP_TIME = 0

topleft = pyautogui.Point(x=929, y=199) # may be different for your monitor!
bottomright = pyautogui.Point(x=1464, y=725) # may be different for your monitor!
deletetoggle = pyautogui.Point(x=380, y=915) # may be different for your monitor!
first_const = pyautogui.Point(x=962, y=239) # may be different for your monitor!
focus = pyautogui.Point(x=382, y=954) # may be different for your monitor!

pos_grid = {}
start_x = 962 # may be different for your monitor!
start_y = 239 # may be different for your monitor!
increment = 75 # may be different for your monitor!
for y in range(7):
    pos_grid[y] = []
    for x in range(7):
        pos_grid[y].append(pyautogui.Point(start_x + increment * x, start_y + increment * y))

print("\nMove your mouse to a point on the load constellations button.")
old_mouse_pos = "old_mouse_pos"
load_empty = ""
while old_mouse_pos != load_empty:
    old_mouse_pos = pyautogui.position()
    time.sleep(1)
    load_empty = pyautogui.position()
time.sleep(2)

print("Move your mouse to the outside constellation focus button.")
old_mouse_pos = "old_mouse_pos"
focus_outside = ""
while old_mouse_pos != focus_outside:
    old_mouse_pos = pyautogui.position()
    time.sleep(1)
    focus_outside = pyautogui.position()

time.sleep(1)
pyautogui.click(focus_outside)
last_diff = ""
completed_round = False
for frame_id, frame in frames.items():
    if not f"frame_{frame_id}.png" in frame_dir_files:
        if str(frame) in cache:
            first_id = cache[str(frame)][0]
            if not f"frame_{frame_id}.png" in frame_dir_files and f"frame_{first_id}.png" in frame_dir_files:
                shutil.copy(f"./screenshots/frame_{first_id}.png", f"./screenshots/frame_{frame_id}.png")
                open("cache.json", "w").write(json.dumps(cache, indent=2))
                continue
    else:
        continue

    if int(frame_id) < 43 or completed_round == False:
        color_all_grid()
        time.sleep(0.5)
        pyautogui.moveTo(x=10, y=10, _pause=False)
        take_ss(frame_id)
        completed_round = True
    else:
        diffed_grid = diff_grid(frames[last_diff], frames[frame_id])
        color_diffed_grid(diffed_grid)

        time.sleep(0.5)
        pyautogui.moveTo(x=10, y=10, _pause=False)
        take_ss(frame_id)

    last_diff = frame_id
