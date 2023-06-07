import cv2 as cv
import numpy as np

def find_template(screenshot, template, threshold=0.8):
  img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
  w, h = template.shape[::-1]
 
  # Perform match operations.
  res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
  
  # Store the coordinates of matched area in a numpy array
  loc = np.where(res >= threshold)

  # Draw a rectangle around the matched region.
  # for pt in zip(*loc[::-1]):
  #     cv.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
  
  # # Show result
  # cv.imshow("Found", screenshot)
  # cv.waitKey(0)

  return loc

