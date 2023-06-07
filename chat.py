import cv2 as cv
import pytesseract

def read_line(screenshot):
  cropped = screenshot[850:865, 505:1050]
  text = pytesseract.image_to_string(cropped, lang="ces")
  print(text)
  cv.imshow("t",cropped)
  cv.waitKey(0)
  return text