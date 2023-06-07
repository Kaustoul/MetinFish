import cv2 as cv
import requests
import json
import time
from vision import find_template

captcha_template = None
captcha_coords = {
  "0": "102x131",
  "1": "56x59",
  "2": "102x59",
  "3": "148x59",
  "4": "56x83",
  "5": "102x83",
  "6": "148x83",
  "7": "56x107",
  "8": "102x107",
  "9": "148x107",
  "Enter": "102x155"
}

async def guess_captcha(image):
  cv.imwrite("0.png", image)
  payload = {
    'isOverlayRequired': False,
    'apikey': "K85412763588957",
    'language': "eng",
    'OCREngine': 5
  }
  with open("0.png", 'rb') as f:
    r = requests.post('https://api.ocr.space/parse/image',
                          files={"0.png": f},
                          data=payload,
                          )
  response = r.content.decode()
  response_json = json.loads(response)
  lines = response_json["ParsedResults"][0]["TextOverlay"]["Lines"]
  
  return None if len(lines) == 0 else lines[0]["LineText"]

captcha_template

def init_captcha():
  global captcha_template
  captcha_template = cv.imread("templates/captcha.png", 0)

async def solve_captcha(hwnd, captcha_x, captcha_y, captcha_text):
  # click on chaptcha to move it to foreground
  await input.click(hwnd, captcha_x + 48, captcha_y + 10)
  for num in captcha_text:
    coords = captcha_coords[num].split('x')
    await input.click(hwnd, captcha_x + int(coords[0]), captcha_y + int(coords[1]))
    time.sleep(0.1)

  enter_coords = captcha_coords["Enter"].split('x')
  await input.click(hwnd, captcha_x + int(enter_coords[0]), captcha_y + int(enter_coords[1]))
  time.sleep(0.1)


async def check_captcha(hwnd, screenshot):
  loc = await find_template(screenshot, captcha_template, threshold=0.5)

  # No captcha found
  if loc[0].any() == False:
    return

  # Take screenshot of only captcha text
  numbers_x = loc[1][0]+48
  numbers_y = loc[0][0]+10
  numbers_img = screenshot[numbers_y:numbers_y+30, numbers_x:numbers_x+40]
  numbers_img = cv.cvtColor(numbers_img, cv.COLOR_BGR2GRAY)

  captcha = await guess_captcha(numbers_img)
  if captcha is None:
    print("Couldnt solve captcha, change channel")
    return
    
  await solve_captcha(hwnd, loc[1][0], loc[0][0], captcha)