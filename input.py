import win32gui, win32api, win32con
import globals
from utils import rand_sleep

codes = {
  "0": 0x30,
  "1": 0x31,
  "2": 0x32,
  "3": 0x33,
  "4": 0x34,
  "5": 0x35,
  "6": 0x36,
  "7": 0x37,
  "8": 0x38,
  "9": 0x39,

  "a": 0x41,
  "b": 0x42,
  "c": 0x43,
  "d": 0x44,
  "e": 0x45,
  "f": 0x46,
  "g": 0x47,
  "h": 0x48,
  "i": 0x49,
  "j": 0x4A,
  "k": 0x4B,
  "l": 0x4C,
  "m": 0x4D,
  "n": 0x4E,
  "o": 0x4F,
  "p": 0x50,
  "q": 0x51,
  "r": 0x52,
  "s": 0x53,
  "t": 0x54,
  "u": 0x55,
  "v": 0x56,
  "w": 0x57,
  "x": 0x58,
  "y": 0x59,
  "z": 0x5A,

  "F1":	0x70,	
  "F2":	0x71,	
  "F3":	0x72,	
  "F4":	0x73,	
  "F5":	0x74,	
  "F6":	0x75,	
  "F7":	0x76,	
  "F8":	0x77,	
  "F9":	0x78,	
  "F10":	0x79
}

def get_code(char):
  return codes[char]

def click(hwnd, x, y, button='left'):
  assert button == 'left' or button == 'right'
  # win32gui.SetForegroundWindow(hwnd)
  
  x = x + globals.windows[hwnd]['x']
  y = y + globals.windows[hwnd]['y']
  
  l_param = win32api.MAKELONG(x, y)
  win32api.SetCursorPos((x, y))
  win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, l_param)
  rand_sleep(0.01, scaling=0.01)

  if button == 'left':
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    rand_sleep(0.01, scaling=0.01)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, l_param)

  elif button == 'right':
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, l_param)
    rand_sleep(0.01, scaling=0.01)
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, l_param)

def send_function_key(hwnd, function_key_number, CTRL=False):
  code = get_code(f"F{function_key_number}")
  virtual_key = win32api.MapVirtualKey(code, 0)

  if CTRL:
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    rand_sleep(0.01, 0.01)

  win32api.keybd_event(win32con.VK_F1, 0, 0, 0)
  rand_sleep(0.01, 0.01)
  win32api.keybd_event(win32con.VK_F1, 0, win32con.KEYEVENTF_KEYUP, 0)
  rand_sleep(0.01, 0.01)

  # Control key press, didnt work for me
  # win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, code, 0x0001|virtual_key<<16)
  # win32api.PostMessage(hwnd, win32con.WM_KEYUP, code, 0x0001|virtual_key<<16|0xC0<<24)
  
  if CTRL:
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    rand_sleep(0.01, 0.01)


def send_ctrl(hwnd, text):
  pass

async def send_shift(hwnd, text):
  pass

def send_keys(hwnd, text, CTRL=False, SHIFT=False):
  if CTRL:
    send_ctrl(hwnd, text)
    return
  
  if SHIFT:
    send_shift(hwnd, text)
    return
  
  for c in text:
    code = get_code(c)
    print(hex(code))
    virtual_key = win32api.MapVirtualKey(code, 0)

    win32api.keybd_event(code, virtual_key, 0, 0)
    rand_sleep(0.01, scaling=0.01)
    win32api.keybd_event(code, virtual_key, win32con.KEYEVENTF_KEYUP, 0)
    rand_sleep(0.01, scaling=0.01)

def send_control_shift(hwnd, text):
  win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)

  for c in text:
    code = get_code(c)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, code, 0x001E0001)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, code, 0xC01E0001)

  win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
  rand_sleep(0.01, scaling=0.01)

def send_control_ctrl(hwnd, text):
  win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)

  for c in text:
    code = get_code(c)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, code, 0x001E0001)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, code, 0xC01E0001)

  win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
  rand_sleep(0.01, scaling=0.01)

# Without having the window in foreground
# The game will not allow to use hotbar spells and items this way
def send_control_keys(hwnd, text, CTRL=False, SHIFT=False):
  if CTRL:
    send_control_ctrl(hwnd, text)
    return
  
  if SHIFT:
    send_control_shift(hwnd, text)
    return
  
  for c in text:
    code = get_code(c)
    
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, code, 0)
    rand_sleep(0.01, scaling=0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, code, 0)
    rand_sleep(0.01, scaling=0.01)
    # win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)    