import pyautogui
import keyboard
import time
import sys
import mss 
from PIL import Image

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Please specify a macro file")
    exit()

class Timer:
    def __init__(self):
        self.curr = time.time_ns()
    
    def get(self):
        return float((time.time_ns() - self.curr) // 1_000_000)

    def reset(self):
        self.curr = time.time_ns()

timer = Timer()

def capture(x, y, w, h):
    with mss.mss() as sct:
        region = {"left": x, "top": y, "width": w, "height": h}
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return img

def within(value, target, threshold):
    return value > (target - threshold) and value < (target + threshold)

def check_gastly(image):
    pixels = image.load()
    purbles = 0
    threshold = 10
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            if within(r, 205, threshold) and within(g, 165, threshold) and within(b, 197, threshold):
                purbles += 1
            else:
                pixels[i, j] = (0, 0, 0)
    return purbles < 3300

def run(cmd):
    global timer
    if keyboard.is_pressed('esc'):
        print("Exiting...")
        exit()
    if cmd == "":
        return
    args = cmd.split(" ")
    lena = len(args)
    if args[0] == "wait":
        waittime = int(args[1])
        timer.reset()
        while timer.get() < waittime:
            if keyboard.is_pressed('esc'):
                print("Exiting...")
                exit()
    elif args[0] == "press":
        if lena != 3:
            print("Invalid format for press command")
            exit()
        pyautogui.keyDown(args[1])
        waittime = int(args[2])
        timer.reset()
        while timer.get() < waittime:
            if keyboard.is_pressed('esc'):
                print("Exiting...")
                exit()
        pyautogui.keyUp(args[1])
    elif args[0] == "click":
        if lena != 4:
            print("Invalid format for click command")
            exit()
        xc = int(args[2])
        yc = int(args[3])
        oldx, oldy = pyautogui.position()
        pyautogui.moveTo(xc, yc)
        pyautogui.click(button=args[1])
        pyautogui.moveTo(oldx, oldy)
    elif args[0] == "check":
        if lena != 6:
            print("Invalid format for check command")
            exit()
        if args[1] == "gastly":
            image = capture(int(args[2]), int(args[3]), int(args[4]), int(args[5]))
            if (check_gastly(image)):
                print("A SHINY WAS FOUND!!")
                exit()
        else:
            print("Unsupported check detected")
            exit()
    else:
        print("invalid macro command detected: " + cmd)
        exit()

lines = []
with open(sys.argv[1], "r") as f:
    lines = f.readlines()

loop = False
if len(sys.argv) == 3:
    if sys.argv[2] == "loop":
        loop = True
    else:
        print("Invalid third arg")
        exit()
if loop:
    while True:
        for line in lines:
            if len(line) > 0 and line[0] == '#':
                continue
            run(line.strip())
else:
    for line in lines:
        if len(line) > 0 and line[0] == '#':
            continue
        run(line.strip())
print("Done running macro!")