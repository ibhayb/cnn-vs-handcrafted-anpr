import cv2 as cv
import numpy as np
import os
import easyocr
import re

def is_likely_plate(text):
    cleaned = ''.join(filter(str.isalnum, text.upper()))
    return bool(re.match(r'^[A-ZÄÖÜ]{1,3}[A-Z]{1,2}[1-9][0-9]{0,3}[HE]?$', cleaned))

def box_area(bbox):
    x0, y0 = bbox[0]
    x2, y2 = bbox[2]
    return abs((x2 - x0) * (y2 - y0))

def preprocess_plate(plate_img):
    gray = cv.cvtColor(plate_img, cv.COLOR_BGR2GRAY)
    denoised = cv.bilateralFilter(gray, 11, 17, 17)
    contrast = cv.convertScaleAbs(denoised, alpha=1.8, beta=0)
    return contrast

image_dir = "../images"
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

reader = easyocr.Reader(['en'])

for filename in image_files:
    img_path = os.path.join(image_dir, filename)
    img = cv.imread(img_path)
    if img is None:
        print(f"Could not read image {img_path}")
        continue

    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(grayscale_img, 100, 200)

    contours, _ = cv.findContours(edges.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    plate_contour = None
    for contour in contours:
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            x, y, w, h = cv.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 2 < aspect_ratio < 6:
                plate_contour = approx
                break

    if plate_contour is not None:
        x, y, w, h = cv.boundingRect(plate_contour)
        plate_image = img[y:y + h, x:x + w]
    else:
        plate_image = img.copy()

    # 🔧 Preprocessing nur auf das gecroppte Kennzeichen anwenden
    plate_for_ocr = preprocess_plate(plate_image)

    # OCR auf dem vorbereiteten Ausschnitt
    results = reader.readtext(plate_for_ocr)

    # Filter zu kleine Boxen (z.B. Sticker, Logos)
    MIN_AREA = 1000
    filtered = [(bbox, text, prob) for (bbox, text, prob) in results if box_area(bbox) >= MIN_AREA]

    texts = []
    for (bbox, text, prob) in filtered:
        cleaned = ''.join(filter(str.isalnum, text.upper()))
        if cleaned:
            texts.append((bbox, cleaned))

    # Sortiere von links nach rechts
    texts = sorted(texts, key=lambda item: min(pt[0] for pt in item[0]))
    full_plate = ''.join([txt for _, txt in texts])

    if is_likely_plate(full_plate):
        print("✅ Erkanntes Kennzeichen:", full_plate)
        for (bbox, text) in texts:
            pts = [tuple(map(int, point)) for point in bbox]
            cv.polylines(plate_image, [np.array(pts)], isClosed=True, color=(0, 255, 0), thickness=2)
            cv.putText(plate_image, text, pts[0], cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    else:
        print("⛔ Kein valides Kennzeichen erkannt.")

    # Anzeigen
    cv.imshow('Original', img)
    cv.imshow('Detected Plate + OCR', plate_image)

    print(f"Showing: {filename}")
    key = cv.waitKey(0)
    if key == 27:
        break

cv.destroyAllWindows()
