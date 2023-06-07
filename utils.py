import globals
import win32gui
from random import random
from time import sleep

def rand_sleep(time, scaling=1):
  time = time + (random() * scaling)
  sleep(time)

def coords_is_empty(coords):
  return not coords[0].any()