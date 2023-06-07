from config import init_config
from windowmanager import init_windows
import globals
import asyncio
import fish
import pytesseract
from captcha import init_captcha
from windowcapture import init_screenshot


def main():
  globals.init()
  globals.cfg = init_config()
  init_windows()
  init_screenshot()
  pytesseract.pytesseract.tesseract_cmd = globals.cfg["PATH"]["Tesseract"]
  init_captcha()

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(fish.main())

  loop.close()



if __name__ == '__main__':
  main()