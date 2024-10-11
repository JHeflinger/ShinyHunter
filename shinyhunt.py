import pyautogui
import keyboard
import time
import sys

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
            run(line.strip())
else:
    for line in lines:
        run(line.strip())
print("Done running macro!")