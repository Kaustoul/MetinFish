import os
import time
import keyboard
import win32api, win32con, win32gui
import cv2 as cv
import numpy as np
from windowcapture import WindowCapture
import tkinter as tk
from enum import Enum
import configparser
import utils

class PickupMode(Enum):
    OFF = 1
    HOLD = 2
    AUTO = 3

pickupMode = PickupMode.OFF
config = None
hwnd = None

def readConfig():
    global pickupMode
    global config
    config.read('config.ini')
    pickupMode = PickupMode[config.get('MetinAssist','PickupMode')]

def saveConfig():
    config['MetinAssist']['PickupMode'] = pickupMode.name
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def close():
    saveConfig()
    exit(0)

def switchPickupMode():
    global pickupMode
    if pickupMode is PickupMode.OFF:
        pickupMode = PickupMode.HOLD
    elif pickupMode is PickupMode.HOLD:
        pickupMode = PickupMode.AUTO
    elif pickupMode is PickupMode.AUTO:
        pickupMode = PickupMode.OFF

    utils.clear()
    utils.printHeader()
    print("PickupMode: ", pickupMode.name)

def everyHalfSec():
    global pickupMode
    if pickupMode is PickupMode.AUTO or (pickupMode is PickupMode.HOLD and keyboard.is_pressed('x')):
        keyboard.press('y')
        keyboard.press('z')

def everySec():
    
    pass

def start():
    utils.clear()
    utils.printHeader()
    print("PickupMode: ", pickupMode.name)
    now = time.time()
    didHalfSec = False
    didSec = False
    
    while True:
        if keyboard.is_pressed('ctrl'): 
            if keyboard.is_pressed('q'):
                close()

            if keyboard.is_pressed('z') or keyboard.is_pressed('y'):
                switchPickupMode()
                if not utils.wait(0.5):
                    close()

        if not didHalfSec and time.time() - now > 0.5:
            everyHalfSec()
            didHalfSec = True
            didSec = False

        if not didSec and time.time() - now > 1:
            everyHalfSec()
            everySec()
            didSec = True
            didHalfSec = False
            now = time.time()


if __name__ == '__main__':
    utils.clear()
    utils.printHeader()
    
    config = configparser.ConfigParser()
    if (not os.path.isfile('./config.ini')):
        config['MetinAssist'] = {'HealthPotionSlot': '2',
                                'ManaPotionSlot': 'f2',
                                'HealthThreshold': '50',
                                'ManaThreshold': '50',
                                'PickupMode': 'OFF'}

        saveConfig()

    readConfig()

    utils.clear()
    hwnd = utils.gethwndArray('metin2')
    if len(hwnd) == 0:
        print("Could not find Metin client. Please start Metin and restart MetinAssist!")
    elif len(hwnd) == 1:
        hwnd = hwnd[0][0]
    else:
        print(f"Found {len(hwnd)} instances of Metin client. Please select one:\n")
        text = input("Press 'Enter' to continue. If you know which procces to choose type the procces number.\n")
        if text != "":
            hwnd = hwnd[int(text) - 1][0]
        else:
            for i in range(0, len(hwnd)):
                utils.clear()
                utils.printHeader()

                print(f"Checking procces: '{i + 1}. {hwnd[i][0]}'\n\n")
                print("You will be 'alt-tabbed' into this window, to check. if this is the one you want MetinAssist to work on.\nPlease 'alt-tab' back into MetinAssist to continue...")
                time.sleep(1)
                input("Press 'Enter' to continue...\n")
                win32gui.ShowWindow(hwnd[i][0], 9)

                time.sleep(1)
                if input("\nType '1' to select this window. Press anything else to continue checking\n") == "1":
                    hwnd = hwnd[i][0]
                    print(f"Selected procces with number {i+1}.")
                    break

                if i+2 == len(hwnd):
                    hwnd = hwnd[i+1][0]
                    print(f"Selected last procces with number {i+2}.")
                    break

    utils.clear()
    utils.printHeader()
    print("Starting...")
    time.sleep(1)
    start()


    