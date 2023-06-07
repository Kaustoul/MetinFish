import win32gui, win32con, win32com.client, win32process
import globals

shell = None

def init_windows():
  global shell
  shell = win32com.client.Dispatch("WScript.Shell")


  def filterMetinWindows(hwnd, results):
    if (win32gui.GetWindowText(hwnd) == "Nitem Client"):
      rect = win32gui.GetWindowRect(hwnd)
    
      globals.windows[hwnd] = {
        "x": rect[0],
        "y": rect[1],
        "w": rect[2] - rect[0],
        "h":  rect[3] - rect[1]}
      
  win32gui.EnumWindows(filterMetinWindows, [])


def set_foreground(hwnd):
  win32gui.SetForegroundWindow(hwnd)
  win32gui.SetActiveWindow(hwnd)

def maximize(hwnd):
  win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

def minimize(hwnd):
  win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def activate(hwnd):
  _, pid = win32process.GetWindowThreadProcessId(hwnd)
  shell.AppActivate(pid)
