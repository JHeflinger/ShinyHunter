import pyautogui
import keyboard
import time
import sys
import mss 
import io
import win32clipboard
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
    return purbles < 3300 and purbles > 100

def wait(duration):
    waittime = duration
    timer.reset()
    while timer.get() < waittime:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            exit()

def keypress(key, duration):
    pyautogui.keyDown(key)
    wait(duration)
    pyautogui.keyUp(key)

def type(message):
    for c in message:
        keypress(c, 1)

def click(buttonstr, x, y):
    oldx, oldy = pyautogui.position()
    pyautogui.moveTo(x, y)
    pyautogui.click(button=buttonstr)
    pyautogui.moveTo(oldx, oldy)

def copy(image):
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def move(x, y):
    pyautogui.moveTo(x, y)

def thousandth(comp, order):
    return comp >= order * 1000 and comp <= (order + 1) * 1000

def colorcheck(x, y, w, h, soft=False):
    while True:
        image = capture(x, y, w, h)
        tr = 0
        tg = 0
        tb = 0
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                tr += r
                tg += g
                tb += b
        color = "black"
        if thousandth(tr, 38) and thousandth(tg, 31) and thousandth(tb, 48):
            color = "purple"
        if thousandth(tr, 49) and thousandth(tg, 10) and thousandth(tb, 15):
            color = "red"
        if thousandth(tr, 27) and thousandth(tg, 39) and thousandth(tb, 20):
            color = "green"
        if thousandth(tr, 19) and thousandth(tg, 38) and thousandth(tb, 53):
            color = "blue"
        if color != "black" or soft:
            return color
        wait(2000)

def standby(x, y, w, h):
    while True:
        color = colorcheck(x, y, w, h)
        if color == "green":
            return
        elif color == "red":
            exit()

def killall():
    pyautogui.keyDown("esc")
    time.sleep(10)
    pyautogui.keyUp("esc")
    exit()

def debug(x, y, w, h):
    color = colorcheck(x, y, w, h, soft=True)
    if color == "blue":
        return True
    elif color == "red":
        killall()
    else:
        return False

def wild(x, y, w, h):
    color = colorcheck(x, y, w, h, soft=True)
    if color == "purple":
        return True
    elif color == "red":
        killall()
    else:
        return False

g_conditional = False
def run(cmd):
    global timer
    global g_conditional
    if keyboard.is_pressed('esc'):
        print("Exiting...")
        exit()
    if cmd == "":
        return
    if not g_conditional and cmd[0] == '>':
        return
    if g_conditional and cmd[0] != '>':
        g_conditional = False
    if g_conditional and cmd[0] == '>':
        cmd = cmd[2:]
    if cmd == "exit":
        exit()
    args = cmd.split(" ")
    lena = len(args)
    if args[0] == "wait":
        wait(int(args[1]))
    elif args[0] == "standby":
        standby(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
    elif args[0] == "copy":
        image = capture(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
        copy(image)
    elif args[0] == "down":
        pyautogui.mouseDown(button=args[1])
    elif args[0] == "up":
        pyautogui.mouseUp(button=args[1])
    elif args[0] == "move":
        move(int(args[1]), int(args[2]))
    elif args[0] == "debug":
        g_conditional = debug(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
    elif args[0] == "wild":
        g_conditional = wild(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
    elif args[0] == "hotkey":
        pyautogui.hotkey(args[1], args[2])
    elif args[0] == "print":
        print(cmd.split("print \"")[1][:-1])
    elif args[0] == "type":
        type(cmd.split("type \"")[1][:-1])
    elif args[0] == "save":
        image = capture(int(args[1]), int(args[2]), int(args[3]), int(args[4]))
        image.save("images/" + str(time.time()) + ".png")
    elif args[0] == "press":
        if lena != 3:
            print("Invalid format for press command")
            exit()
        keypress(args[1], int(args[2]))
    elif args[0] == "click":
        if lena != 4:
            print("Invalid format for click command")
            exit()
        click(args[1], int(args[2]), int(args[3]))
    elif args[0] == "check":
        if lena != 6:
            print("Invalid format for check command")
            exit()
        if args[1] == "gastly":
            image = capture(int(args[2]), int(args[3]), int(args[4]), int(args[5]))
            copy(image)
            g_conditional = check_gastly(image)
        else:
            print("Unsupported check detected")
            exit()
    else:
        print("invalid macro command detected: " + cmd)
        exit()

lines = []
with open(sys.argv[1], "r") as f:
    lines = f.readlines()

def play_commands(lines):
    ltimer = Timer()
    for line in lines:
        if len(line) > 0 and line[0] == '#':
            continue
        run(line.strip())
    print(f"Executed macro in {ltimer.get() / 1000} seconds")
    counter = 18
    with open(".time", "r") as f:
        counter += int(str(f.read()).strip())
    with open(".time", "w") as f:
        f.write(str(counter))

loop = False
if len(sys.argv) == 3:
    if sys.argv[2] == "loop":
        loop = True
    else:
        print("Invalid third arg")
        exit()
if loop:
    while True:
        play_commands(lines)
else:
    play_commands(lines)
print("Done running macro!")