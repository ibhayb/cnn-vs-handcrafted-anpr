import cv2 as cv
import numpy as np
import math

# def is_rectangle(approx, angle_tolerance=10):
#     if len(approx) < 4:
#         return False

#     def angle(pt1, pt2, pt0):
#         dx1 = pt1[0][0] - pt0[0][0]
#         dy1 = pt1[0][1] - pt0[0][1]
#         dx2 = pt2[0][0] - pt0[0][0]
#         dy2 = pt2[0][1] - pt0[0][1]
#         dot = dx1 * dx2 + dy1 * dy2
#         mag1 = math.hypot(dx1, dy1)
#         mag2 = math.hypot(dx2, dy2)
#         cos_angle = dot / (mag1 * mag2 + 1e-10)
#         angle_rad = math.acos(max(min(cos_angle, 1), -1))
#         return math.degrees(angle_rad)

#     angles = [angle(approx[(i+1)%4], approx[(i-1)%4], approx[i]) for i in range(4)]
#     return all(abs(a - 90) < angle_tolerance for a in angles)

# Video laden
cap = cv.VideoCapture("test.mov")
if not cap.isOpened():
    print("Video konnte nicht geöffnet werden.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.bilateralFilter(gray, 11, 75, 75)
    edges = cv.Canny(blurred, 170, 200)

    # Kanten "vervollständigen"
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    closed = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    # Konturen im "closed"-Bild finden
    contours, _ = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # # Kopie des Bildes zur Anzeige
    # output = frame.copy()

    # # Alle gefundenen Konturen zeichnen
    # cv.drawContours(output, contours, -1, (0, 255, 0), 2)

    # # Anzeigen
    # cv.imshow("Gefundene geschlossene Objekte", output)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    rect_img = frame.copy()
    for contour in contours:
        if cv.contourArea(contour) < 1000:
            continue  # Rausfiltern kleiner Objekte

        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        x, y, w, h = cv.boundingRect(approx)
        aspect_ratio = w / float(h)

        if 2 < aspect_ratio < 6:
            cv.rectangle(rect_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            plate_image = frame[y:y + h, x:x + w]
            cv.imshow("Kennzeichen", plate_image)

    # Anzeigen
    cv.imshow("Kanten geschlossen", closed)
    cv.imshow("Gefundene Rechtecke", rect_img)

    key = cv.waitKey(0)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()
