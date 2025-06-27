# libraries
from ultralytics import YOLO
import cv2 as cv

# load trained model
model = YOLO('/home/kreso/Desktop/bild/cnn-vs-handcrafted-anpr/cnn/best.pt')

# start webcam
cap = cv.VideoCapture(0)

# analyze frames: frame by frame
while True:
    success, frame = cap.read()
    results = model(frame, stream = True, conf = 0.5)

    # extract bboxes
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # bbox coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # confidence value
            conf = float(box.conf[0])
            conf_text = f'{conf:.2f}'

            # label (Kennzeichen)
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            # draw rectangle and text
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.putText(frame, f'{label} {conf_text}', (x1, y1 - 10),
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # show frame
    cv.imshow('YOLOv8 Webcam Detection', frame)

    # break with q
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap.release()
cv.destroyAllWindows()
