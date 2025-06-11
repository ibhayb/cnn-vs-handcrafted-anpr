import cv2 as cv
import numpy as np
import os

image_dir = "../images"
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for filename in image_files:
    img_path = os.path.join(image_dir, filename)
    img = cv.imread(img_path)
    if img is None:
        print(f"Could not read image {img_path}")
        continue

    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # blurred = cv.GaussianBlur(grayscale_img, (3, 3), 0)
    edges = cv.Canny(grayscale_img, 100, 200)

    contours, _ = cv.findContours(edges.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    plate_contour = None

    for contour in contours:
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        cv.drawContours(img, [approx], -1, (0, 255, 0), 5)
        if len(approx) == 4:
            x, y, w, h = cv.boundingRect(approx)
            aspect_ratio = w / float(h)
            print(f"Processing contour with {len(approx)} points, Aspect Ratio: {aspect_ratio:.2f}")
            print(f"Contour: {len(approx)} points, Aspect Ratio: {aspect_ratio:.2f}")
            if 2 < aspect_ratio < 6:
                plate_contour = approx
                break

    if plate_contour is not None:
        x, y, w, h = cv.boundingRect(plate_contour)
        plate_image = grayscale_img[y:y + h, x:x + w]
    else:
        plate_image = grayscale_img  # fallback

    # show original in one window
    cv.imshow('Original', img)

    # show detected plate or fallback in another window
    cv.imshow('Detected Plate', plate_image)

    print(f"Showing: {filename}")
    key = cv.waitKey(0)
    if key == 27:  # ESC
        break

cv.destroyAllWindows()
