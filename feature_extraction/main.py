# libraries
import cv2 as cv
import numpy as np

# load the image
img_path = "/Users/kresovic/Documents/Uni/Master/2.Semester/Bild/Projekt/images/hell_vorne2.jpeg"
img = cv.imread(img_path)

# convert to grayscale
grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# blur to reduce noise
blurred = cv.GaussianBlur(grayscale_img, (5, 5), 0)

# canny edge detection
edges = cv.Canny(blurred, 100, 200)

contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key=cv.contourArea, reverse=True)
plate_contour = None
for contour in contours:
    epsilon = 0.02 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        plate_contour = approx
        break

x, y, w, h = cv.boundingRect(plate_contour)
plate_image = grayscale_img[y:y + h, x:x + w]

# display image
cv.imshow('edges',plate_image)
cv.waitKey(0)
