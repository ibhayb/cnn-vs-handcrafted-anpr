import cv2 as cv
import numpy as np
import os
import easyocr
import re

def show_traffic_light(is_allowed: bool):
    # Erstelle leeres schwarzes Bild
    light = np.zeros((200, 100, 3), dtype=np.uint8)

    # Farben definieren
    red_on = (0, 0, 255)
    yellow_on = (0, 255, 255)
    green_on = (0, 255, 0)
    off = (50, 50, 50)

    # Ampellogik:
    if is_allowed:
        colors = [off, off, green_on]  # nur grün leuchtet
    else:
        colors = [red_on, off, off]    # nur rot leuchtet

    # Kreise zeichnen (oben: rot, mitte: gelb, unten: grün)
    positions = [(50, 40), (50, 100), (50, 160)]
    for pos, color in zip(positions, colors):
        cv.circle(light, pos, 20, color, -1)

    # Fenster anzeigen
    cv.imshow("Traffic Light", light)

def is_likely_plate(text):
    cleaned = ''.join(filter(str.isalnum, text.upper()))
    return bool(re.match(r'^[A-ZÄÖÜ]{1,3}[A-Z]{1,2}[1-9][0-9]{0,3}[HE]?$', cleaned))

def extract_plate(text):
    cleaned = ''.join(filter(str.isalnum, text.upper()))
    matches = re.findall(r'[A-ZÄÖÜ]{1,3}[A-Z]{1,2}[1-9][0-9]{0,3}[HE]?$', cleaned)
    return matches[0] if matches else None

def box_area(bbox):
    x0, y0 = bbox[0]
    x2, y2 = bbox[2]
    return abs((x2 - x0) * (y2 - y0))

def box_height(bbox):
    return abs(bbox[2][1] - bbox[0][1])

def preprocess_plate(plate_img):
    gray = cv.cvtColor(plate_img, cv.COLOR_BGR2GRAY)
    denoised = cv.bilateralFilter(gray, 11, 17, 17)
    contrast = cv.convertScaleAbs(denoised, alpha=1.8, beta=0)
    return contrast

image_dir = "../images"
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
white_listed_plates = ['FES2467', 'FES2761', ]

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
    # plate_for_ocr = preprocess_plate(plate_image)

    # OCR auf dem vorbereiteten Ausschnitt
    results = reader.readtext(plate_image)

    heights = [box_height(bbox) for (bbox, _, _) in results]
    if heights:
        # Normiere die Höhen, um die Filterung zu ermöglichen
        max_height = max(heights)

        # Filter: Nur Boxen mit normierter Höhe ≥ 0.6
        MIN_NORM_HEIGHT = 0.5
        filtered = []
        for (bbox, text, prob), h in zip(results, heights):
            norm_height = h / max_height if max_height > 0 else 0
            print(norm_height, text, prob)
            if norm_height >= MIN_NORM_HEIGHT:
                filtered.append((bbox, text, prob))


    texts = []
    for (bbox, text, prob) in filtered:
        cleaned = ''.join(filter(str.isalnum, text.upper()))
        if cleaned:
            texts.append((bbox, cleaned))

    # Sortiere von links nach rechts
    texts = sorted(texts, key=lambda item: min(pt[0] for pt in item[0]))
    full_plate = ''.join([txt for _, txt in texts])
    print(full_plate)

    plate_candidate = extract_plate(full_plate)

    print("✅ Erkanntes Kennzeichen:", plate_candidate)
    for (bbox, text) in texts:
        pts = [tuple(map(int, point)) for point in bbox]
        cv.polylines(plate_image, [np.array(pts)], isClosed=True, color=(0, 255, 0), thickness=2)
        text_position = (pts[0][0], pts[0][1] + 30)
        cv.putText(plate_image, text, text_position, cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

    if plate_candidate in white_listed_plates:
        show_traffic_light(True)
    else:
        show_traffic_light(False)
    cv.imshow('Original', img)
    cv.imshow('Detected Plate + OCR', plate_image)

    print(f"Showing: {filename}")
    key = cv.waitKey(0)
    if key == 27:
        break

cv.destroyAllWindows()
