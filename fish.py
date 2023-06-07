import globals
import cv2 as cv
import windowcapture
from captcha import check_captcha
from chat import read_line
import input
from utils import rand_sleep, coords_is_empty
from windowmanager import activate
from vision import find_template

paste_template = None
worm_template = None
fish_ball_template = None
fish_ball_effect_template = None

slots = {}

def init_fish():
  global paste_template, worm_template, fish_ball_template
  paste_template = cv.imread("templates/paste.png", 0)
  worm_template = cv.imread("templates/worm.png", 0)
  fish_ball_template = cv.imread("templates/fish-ball.png", 0)
  fish_ball_effect_template = cv.imread("templates/fish-ball-effect.png", 0)

def convert_slot_index(slot_index):
  if (slot_index < 4):
    return str(slot_index + 1)
  else:
    return f"F{slot_index - 3}"

def find_slot(item_type):
  for slot, value in slots.items():
    if value == item_type:
      return convert_slot_index(slot)

  return None

def is_fish_ball_effect(screenshot):
  ball_effect_coords = find_template(screenshot, fish_ball_effect_template)
  return not coords_is_empty(ball_effect_coords)

def activate_fish_ball(hwnd):
  slot = find_slot("ball")
  # activate(hwnd)
  input.send_keys(hwnd, slot)

def is_bait(slot_img):
  paste_coords = find_template(slot_img, paste_template)
  worm_coords = find_template(slot_img, worm_template, threshold=0.5)
  return not coords_is_empty(paste_coords) or not coords_is_empty(worm_coords)

def is_fish_ball(slot_img):
  ball_coords = find_template(slot_img, fish_ball_template)
  return not coords_is_empty(ball_coords)

# Window must be first activated
def put_bait(hwnd):
  slot = find_slot("bait")
  input.send_keys(hwnd, slot)

def decode_item(slot_img):
  if is_bait(slot_img):
    return "bait"
  
  if is_fish_ball(slot_img):
    return "ball"

  return "none"

def parse_toolbar(screenshot):
  global slots
  cropped_toolbar = screenshot[890:1000, 717:986]

  for i in range(8):
    offset = 0 if i < 4 else 14
  
    cropped_slot = cropped_toolbar[0:110, (i)*32 + offset : (i+1)*32 + offset]
    slots[i] = decode_item(cropped_slot)

def fish_loop(hwnd):
  screenshot = windowcapture.screenshot(hwnd)

  #Check for fish-ball effect
  if not is_fish_ball_effect:
    activate_fish_ball(hwnd)

  #TODO

async def main():
  init_fish()
  hwnd = list(globals.windows.keys())[0]

  while True:
    fish_loop(hwnd)
  # await set_foreground(hwnd)

  # code = input.get_code("1")
  # print(code)
  # virtual_map = win32api.MapVirtualKey(0x31, 0)
  # win32api.keybd_event(0x31, virtual_map, 0, 0)
  # rand_sleep(0.1, 0.1)
  # win32api.keybd_event(0x31, virtual_map, win32con.KEYEVENTF_KEYUP, 0)

  # activate(hwnd)
  # input.send_keys(hwnd, "4")

  parse_toolbar(screenshot)