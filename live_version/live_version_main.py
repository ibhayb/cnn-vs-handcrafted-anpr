import cv2 as cv

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Frame not read correctly!")
        break

    # convert img to grayscale
    grayscale_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # adaptive thresholding --> img into black and white
    thresh = cv.adaptiveThreshold(grayscale_img, 255,
                                cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 11, 2)

    # gaussian blur to remove noise
    #blurred = cv.bilateralFilter(thresh, 9, 75, 75 )
    blurred = cv.GaussianBlur(thresh, (15, 15), 0)

    # canny to detect edges
    edges = cv.Canny(blurred, 100, 200)

    # Kanten "vervollständigen"
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    closed = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    # find contours
    contours, _ = cv.findContours(closed.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # Kopie des Bildes zur Anzeige
    output = frame.copy()

    # Alle gefundenen Konturen zeichnen
    cv.drawContours(output, contours, -1, (0, 255, 0), 2)

    # Anzeigen
    cv.imshow("Gefundene geschlossene Objekte", output)
    cv.waitKey(0)
    cv.destroyAllWindows()

    plate_contour = None

    for contour in contours:
        if cv.contourArea(contour) < 1000:
            continue  # Rausfiltern kleiner Objekte
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        # cv.drawContours(frame, [approx], -1, (0, 255, 0), 5)
        #if 4 <= len(approx) <= 6:
        x, y, w, h = cv.boundingRect(approx)
        aspect_ratio = w / float(h)
        # print(f"Processing contour with {len(contour)} points, Aspect Ratio: {aspect_ratio:.2f}")
        # print(f"Contour: {len(contour)} points, Aspect Ratio: {aspect_ratio:.2f}")
        if 2 <= aspect_ratio <= 6:
            plate_contour = contour
            break

    if plate_contour is not None:
        x, y, w, h = cv.boundingRect(plate_contour)
        plate_image = grayscale_img[y:y + h, x:x + w]
        print(f"Processing contour with {len(plate_contour)} points, Aspect Ratio: {aspect_ratio:.2f}")
        print(f"Contour: {len(plate_contour)} points, Aspect Ratio: {aspect_ratio:.2f}")
    else:
        plate_image = grayscale_img  # fallback

    cv.imshow('Detected Plate', plate_image)
    # # blurred = cv.GaussianBlur(grayscale_img, (3, 3), 0)
    # edges = cv.Canny(grayscale_img, 100, 200)

    # contours, _ = cv.findContours(edges.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv.contourArea, reverse=True)

    # plate_contour = None

    # for contour in contours:
    #     epsilon = 0.02 * cv.arcLength(contour, True)
    #     approx = cv.approxPolyDP(contour, epsilon, True)
    #     cv.drawContours(frame, [approx], -1, (0, 255, 0), 5)
    #     if len(approx) == 4:
    #         x, y, w, h = cv.boundingRect(approx)
    #         aspect_ratio = w / float(h)
    #         print(f"Processing contour with {len(approx)} points, Aspect Ratio: {aspect_ratio:.2f}")
    #         print(f"Contour: {len(approx)} points, Aspect Ratio: {aspect_ratio:.2f}")
    #         if 2 < aspect_ratio < 6:
    #             plate_contour = approx
    #             break

    # if plate_contour is not None:
    #     x, y, w, h = cv.boundingRect(plate_contour)
    #     plate_image = grayscale_img[y:y + h, x:x + w]
    # else:
    #     plate_image = grayscale_img  # fallback

    # # show original in one window
    # cv.imshow('Original', frame)

    # # show detected plate or fallback in another window
    # cv.imshow('Detected Plate', plate_image)

    key = cv.waitKey(0)
    if key == 27:  # ESC
        break

cv.destroyAllWindows()
