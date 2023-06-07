import cv2 as cv
import numpy as np

def none():
    pass

img = cv.imread("test.png")
img = np.array(img)
# img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

cv.imshow('Image', img)

cv.namedWindow('Mask')

cv.createTrackbar('H', 'Mask', 0, 255, none)
cv.createTrackbar('S', 'Mask', 0, 255, none)
cv.createTrackbar('V', 'Mask', 0, 255, none)
cv.createTrackbar('A', 'Mask', 10, 100, none)

while True:
    h = cv.getTrackbarPos('H', 'Mask')
    s = cv.getTrackbarPos('S', 'Mask')
    v = cv.getTrackbarPos('V', 'Mask')
    a = cv.getTrackbarPos('A', 'Mask')


    mask = cv.inRange(img, np.array([h-a, s-a, v-a]), np.array([h+a, s+a, v+a]))
    cv.imshow('Mask', mask)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
