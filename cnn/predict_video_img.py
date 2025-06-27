# libraries
from ultralytics import YOLO
import cv2 as cv
from util import *

# paths
path_model = '/home/kreso/Desktop/bild/cnn-vs-handcrafted-anpr/cnn/best.pt'
fes_video_path = '/home/kreso/Desktop/predict_video/test_neu.mp4'
img_path = '/home/kreso/Desktop/predict_img'

# load trained model and ocr
model = YOLO(path_model)
ocr = initialize_ocr()

# predictions version
video_version = True
image_version = False

# IMAGE VERSION
if image_version:
    results = model.predict(source = img_path,
                            save = True,
                            project = '/home/kreso/Desktop/results',
                            name = 'img')

    # Alle Bilder durchgehen
    for result in results:
        im0 = result.orig_img      # Originalbild
        boxes = result.boxes

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                # Bounding Box ausschneiden
                plate = im0[y1:y2, x1:x2]

                # OCR anwenden
                result = ocr.ocr(plate, det=False, cls=False)
                score, label = extract_ocr_information(result)
                print(f"Kennzeichen: {label}  und Konfidenzwert: {score}")

                # Zeige das erkannte Nummernschild
                cv.imshow("Kennzeichen", plate)
                key = cv.waitKey(0)  # Warte auf Tastendruck
                if key == ord('q'):
                    break

    cv.destroyAllWindows()
    
    


# VIDEO VERSION
if video_version:

    cap = cv.VideoCapture(fes_video_path)
    frame_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1

        # Nur jedes 10. Frame an YOLO schicken
        if frame_count % 20 != 0:
            continue

        # YOLO Vorhersage auf Einzelbild
        results = model.predict(source=frame, conf=0.7, verbose=False)

        for result in results:
            boxes = result.boxes

            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])

                    # Bounding Box ausschneiden
                    plate = frame[y1:y2, x1:x2]

                    # OCR anwenden
                    ocr_result = ocr.ocr(plate, det=False, cls=False)
                    score, label = extract_ocr_information(ocr_result)

                    print(f"[Frame {frame_count}] Kennzeichen: {label}  | Score: {score:.2f}")

                    # Zeichne Bounding Box
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Text (Kennzeichen und Score)
                    text = f"{label} ({score:.2f})"
                    cv.putText(frame, text, (x1, y1 - 10),
                               cv.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

            # Zeige annotiertes Frame
            cv.imshow("YOLOv8 Prediction", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

