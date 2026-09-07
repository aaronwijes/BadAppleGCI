# renderer v1 - 73.38068008422852s (f0 - f100)
# renderer v2 - 49.787747859954834s (f0 - f100)

import pyautogui
import json
import time
import mss
import mss.tools
import os
import shutil

from pynput.mouse import Controller, Button
mouse = Controller()

def take_ss(frame):
    with mss.MSS() as sct:
        region = {"left": 928, "top": 200, "width": 535, "height": 530}
        output = f"./screenshots/frame_{frame}.png"
        sct_img = sct.grab(region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

if not os.path.exists("./screenshots/"):
    os.makedirs("./screenshots/")

frames = json.loads(open("frames.json", "r").read())
cache = json.loads(open("cache.json").read())

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
                    mouse.position = pos_grid[a][b]
                    pyautogui.sleep(0.01)
                    mouse.click(Button.left, 1)
                    pyautogui.sleep(0.02)

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
    if fill_needed(diffed_grid):
        for y, row in enumerate(diffed_grid.values()):
            for x, entry in enumerate(row):
                if entry == 1:
                    mouse.position = pos_grid[y][x]
                    pyautogui.sleep(0.01)
                    mouse.click(Button.left, 1)
                    pyautogui.sleep(0.02)

    if delete_needed(diffed_grid):
        mouse.position = deletetoggle
        pyautogui.sleep(0.01)
        mouse.click(Button.left)
        pyautogui.sleep(0.02)

        pyautogui.sleep(0.05)
        for y, row in enumerate(diffed_grid.values()):
            for x, entry in enumerate(row):
                if entry == 0:
                    mouse.position = pos_grid[y][x]
                    pyautogui.sleep(0.01)
                    mouse.click(Button.left, 1)
                    pyautogui.sleep(0.02)

        mouse.position = deletetoggle
        pyautogui.sleep(0.01)
        mouse.click(Button.left)
        pyautogui.sleep(0.02)

    if fill_needed(diffed_grid) or delete_needed(diffed_grid):
        pyautogui.sleep(0.05)

# use this code in a python shell to get current mouse position:
# import time,pyautogui;time.sleep(3);print(pyautogui.position())
pyautogui.DARWIN_CATCH_UP_TIME = 0

deletetoggle = (380, 915) # may be different for your monitor!

pos_grid = {}
start_x = 962 # may be different for your monitor!
start_y = 239 # may be different for your monitor!
increment = 75 # may be different for your monitor!
for y in range(7):
    pos_grid[y] = []
    for x in range(7):
        pos_grid[y].append((start_x + increment * x, start_y + increment * y))

time.sleep(1)
last_diff = ""
completed_round = False
for frame_id, frame in frames.items():
    frame_dir_files = os.listdir("./screenshots/")
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
        mouse.position = (100, 100)
        pyautogui.sleep(0.05)
        take_ss(frame_id)
        completed_round = True
    else:
        diffed_grid = diff_grid(frames[last_diff], frames[frame_id])
        color_diffed_grid(diffed_grid)

        mouse.position = (100, 100)
        pyautogui.sleep(0.05)
        take_ss(frame_id)

    pyautogui.failSafeCheck()
    last_diff = frame_id
