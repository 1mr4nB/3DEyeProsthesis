import cv2 as cv
import numpy as np
import CoordinatenVinden
import RotateImage
path = r'D:\Skorro\P&O Biomed\Oogfotos\Yannick Resize 25%.jpg'
path = r'D:\Skorro\P&O Biomed\Oogfotos\Job 2.JPG'

foto1 = cv.imread(path, 1)

# Resizing
resized = cv.resize(foto1, (750, 500), interpolation=cv.INTER_CUBIC)
# Breedte in functie van hoogte: 4800 / 3200 * hoogte
# Hoogte in functie van breedte: 3200/4800 * breedte

def empty(a):
        pass

canny = cv.Canny(resized, 0, 200)

cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 240)
cv.createTrackbar("Canny min", "Trackbars",  -255, 255, empty)
cv.createTrackbar("Canny max", "Trackbars",  255, 255, empty)


while True:
        imgGray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(resized, (5,5), cv.BORDER_DEFAULT)
        Canny_min = cv.getTrackbarPos("Canny min", "Trackbars")
        Canny_max = cv.getTrackbarPos("Canny max", "Trackbars")
        imgCanny = cv.Canny(blur, Canny_min, Canny_max)

        cv.imshow("Original", resized)
        cv.imshow("Blur", blur)
        cv.imshow("Canny", imgCanny)
        cv.waitKey(1)

        contours, hierarchies = cv.findContours(imgCanny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

