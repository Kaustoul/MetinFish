import os
import win32gui
import time
import keyboard

toplist, winlist = [], []

clear = lambda: os.system('cls')

def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def gethwnd(name, x):
    win32gui.EnumWindows(enum_cb, toplist)  
    app = [(hwnd, title) for hwnd, title in winlist if name.lower() in title.lower()]
    app = app[x]
    return app[0]

def gethwndArray(name):
    win32gui.EnumWindows(enum_cb, toplist)  
    return [(hwnd, title) for hwnd, title in winlist if name.lower() in title.lower()]

def printHeader():
    print("---===  MetinAssist  ===---\n\n\n")

def wait(sec):
    now = time.time()

    while True:
        if keyboard.is_pressed('q'):
            return False

        if time.time() - now >= sec:
            return True
