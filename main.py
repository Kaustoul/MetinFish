import os
import time
import keyboard
import win32api, win32con, win32gui, win32com.client
import cv2 as cv
import numpy as np
from click import PressAndRelease
from windowcapture import WindowCapture
import tkinter as tk
from enum import Enum
from datetime import datetime

# 586 1000 1333 1033 747 33

startX = 373
startY = 200
sizeX = 170
sizeY = 150

chatX = 586
chatY = 1000
chatSizeX = 747
chatSizeY = 33

wincap = None
chatcap = None

lower = np.array([111, 82, 47])
upper = np.array([141, 112, 67])

lower_red = np.array([203,157,188])
upper_red = np.array([223,177,208])

lower_blue = np.array([209, 137, 40])
upper_blue = np.array([229, 157, 60])

toplist, winlist = [], []

root = tk.Tk()

timer = time.time()

label = None
labelText = tk.StringVar()

class attempts:
    attemptNum = 0
    slotNum = 0

    def updateAttemptNum(self):
        self.attemptNum += 1
        self.slotNum += 1

att = attempts

def setupLabel():
    label = tk.Label(textvariable=labelText, font=('Times New Roman','20'), fg='white', bg='black')
    # label = tk.Label(root, text="test", font=('Times New Roman','32'), fg='black', bg='white')

    label.master.overrideredirect(True)
    label.master.geometry("+1000+250")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")
    label.pack()

    updateLabel(Status.STARTING)


def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def gethwnd(name):
    win32gui.EnumWindows(enum_cb, toplist)  
    firefox = [(hwnd, title) for hwnd, title in winlist if 'METIN2' in title]
    firefox = firefox[0]
    return firefox[0]

# def prepare():s
#     print("Preparing")
#     labelText.set(f"Putting bait on the rod\n Attempt number: {att.attemptNum}\n Time: {np.round(time.time() - timer, 0)}sec\nHold 'q' to exit")
#     root.update()
#     PressAndRelease('1')
#     time.sleep(0.5)
#     PressAndRelease(' ')
#     time.sleep(2)
#     fish()
    
def none():
    pass

class Status(Enum):
    STARTING = 0
    PREPARING = 1
    WAITING = 2
    FISHING = 3
    PULLING = 4
    PAUSED = 5

def statusString(x):
    return {
        0: "Starting MetinFish!",
        1: "Putting bait on the rod",
        2: "Waiting for fish to show up",
        3: "Catching the fish",
        4: "Pulling out the fish",
        5: "PAUSED"
    }[x]

def updateLabel(status):
    labelText.set(f"{statusString(status.value)}\nAttempt: {att.attemptNum}\nLapsed time: {datetime.fromtimestamp(time.time() - timer).strftime('%I:%M:%S')}")
    root.update()

def close():
    cv.destroyAllWindows()
    root.destroy()
    print("Ended")
    exit(0)


def wait(x, status, checkp = True):
    now = time.time()

    while True:
        if keyboard.is_pressed('q'):
            close()

        if time.time() - now >= x:
            return True

        if checkp and keyboard.is_pressed('p') and status is not Status.PAUSED:
            return False

        updateLabel(status)

def getSlot(slot):
    return {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: 'f1',
        6: 'f2',
        7: 'f3',
        8: 'f4'
    }[slot]

def fish():
    clear()
    print("MetinFish Bot Active!\n > Press 'p' to pause\n > Press 'q' to exit")

    delay = 0
    maskBlue = None
    status = Status.STARTING
    slot = 1
    failcount = 0
    shell = win32com.client.Dispatch("Wscript.Shell")
    shell.AppActivate("METIN2")

    while True:
        if keyboard.is_pressed('q'):
            break

        if keyboard.is_pressed('p'):
            if status is not Status.PAUSED:
                status = Status.PAUSED
            else:
                maskBlue = None
                status = Status.PREPARING

            wait(1, status, False)
    
        
        if maskBlue is not None:
            if status is not Status.FISHING and cv.findNonZero(maskBlue) is not None:
                status = Status.FISHING
                delay = 0 
                att.updateAttemptNum(att)

                if att.slotNum >= 200:
                    att.slotNum = 0
                    slot += 1
                    if (slot > 8):
                        close()

            elif status is Status.FISHING and cv.findNonZero(maskBlue) is None:
                status = Status.PULLING

        updateLabel(status)

        if status is Status.STARTING:
            status = Status.PREPARING

        elif status is Status.PREPARING:
            if not wait(0.5, status):
                status = Status.PAUSED
                continue
            win32api.keybd_event(0x31, win32api.MapVirtualKey(0x31, 0), 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x31, win32api.MapVirtualKey(0x31, 0), win32con.KEYEVENTF_KEYUP, 0)
            if not wait(0.5, status):
                status = Status.PAUSED
                continue                
            win32api.keybd_event(0x20, win32api.MapVirtualKey(0x20, 0), 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(0x20, win32api.MapVirtualKey(0x20, 0), win32con.KEYEVENTF_KEYUP, 0)

            delay = time.time()
            status = Status.WAITING

        elif status is Status.WAITING:
            pic = wincap.get_screenshot()
            maskBlue = cv.inRange(pic, lower_blue, upper_blue)

            if time.time() - delay > 5:
                status = Status.PREPARING
                failcount += 1

                win32api.keybd_event(0x31, win32api.MapVirtualKey(0x31, 0), 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(0x31, win32api.MapVirtualKey(0x31, 0), win32con.KEYEVENTF_KEYUP, 0)
                if not wait(0.5, status):
                    status = Status.PAUSED
                    continue                
                win32api.keybd_event(0x20, win32api.MapVirtualKey(0x20, 0), 0, 0)
                time.sleep(0.05)
                win32api.keybd_event(0x20, win32api.MapVirtualKey(0x20, 0), win32con.KEYEVENTF_KEYUP, 0)

                if not wait(1, status):
                    status = Status.PAUSED
                    continue

                if failcount >= 5:
                    slot += 1
                    failcount = 0

        elif status is Status.FISHING:
            failcount = 0
            pic = wincap.get_screenshot()
        
            mask = cv.inRange(pic ,lower, upper)
            maskRed = cv.inRange(pic, lower_red, upper_red)
            maskBlue = cv.inRange(pic, lower_blue, upper_blue)

            result = cv.findNonZero(mask)
            resultRed = cv.findNonZero(maskRed)

            if result is None:
                continue

            x = 0
            y = 0

            for element in result:
                x += element[0][0]
                y += element[0][1]

            x = x / len(result)
            y = y / len(result)

            win32api.SetCursorPos((startX + (int(x)), startY + (int(y))))
            delay -= time.time() - delay

            if delay <= 0 and resultRed is not None:
                cv.imwrite('test.png', pic)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                delay = time.time()

        elif status is Status.PULLING:
            if maskBlue is not None:
                maskBlue = None

            if not wait(1, status):
                status = Status.PAUSED
                continue

            # win32gui.ShowWindow(hwnd, 6)
            # if not wait(2, status):
            #     status = Status.PAUSED
            #     continue
            # win32gui.ShowWindow(hwnd, 9)
            if not wait(2, status):
                status = Status.PAUSED1
                continue

            status = Status.PREPARING

    close()

clear = lambda: os.system('cls')

if __name__ == "__main__":
    clear()
    hwnd = gethwnd("METIN2")
    wincap = WindowCapture(hwnd, startX, startY, startX + sizeX, startY + sizeY)
    chatcap = WindowCapture(hwnd, chatX, chatY, chatX + chatSizeX, chatY + chatSizeY)
    print("\n----=== Welcome to MetinFish Bot ===---- \n\n > developed by FrajerRadek\n\nPress 'Enter' to start the bot.")
    setupLabel()
    keyboard.wait('enter')
    win32gui.ShowWindow(hwnd, 9)
    print("Starting in 3sec")
    wait(3, Status.STARTING)
    fish()
